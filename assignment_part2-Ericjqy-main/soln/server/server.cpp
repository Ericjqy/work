#include <iostream>
#include <cassert>
#include <fstream>
#include <string>
#include <list>

#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <cstring>

#include "wdigraph.h"
#include "dijkstra.h"

struct Point {
    long long lat, lon;
};

// return the manhattan distance between the two points
long long manhattan(const Point& pt1, const Point& pt2) {
  long long dLat = pt1.lat - pt2.lat, dLon = pt1.lon - pt2.lon;
  return abs(dLat) + abs(dLon);
}

// find the ID of the point that is closest to the given point "pt"
int findClosest(const Point& pt, const unordered_map<int, Point>& points) {
  pair<int, Point> best = *points.begin();

  for (const auto& check : points) {
    if (manhattan(pt, check.second) < manhattan(pt, best.second)) {
      best = check;
    }
  }
  return best.first;
}

// read the graph from the file that has the same format as the "Edmonton graph" file
void readGraph(const string& filename, WDigraph& g, unordered_map<int, Point>& points) {
  ifstream fin(filename);
  string line;

  while (getline(fin, line)) {
    // split the string around the commas, there will be 4 substrings either way
    string p[4];
    int at = 0;
    for (auto c : line) {
      if (c == ',') {
        // start new string
        ++at;
      }
      else {
        // append character to the string we are building
        p[at] += c;
      }
    }

    if (at != 3) {
      // empty line
      break;
    }

    if (p[0] == "V") {
      // new Point
      int id = stoi(p[1]);
      assert(id == stoll(p[1])); // sanity check: asserts if some id is not 32-bit
      points[id].lat = static_cast<long long>(stod(p[2])*100000);
      points[id].lon = static_cast<long long>(stod(p[3])*100000);
      g.addVertex(id);
    }
    else {
      // new directed edge
      int u = stoi(p[1]), v = stoi(p[2]);
      g.addEdge(u, v, manhattan(points[u], points[v]));
    }
  }
}

int create_and_open_fifo(const char * pname, int mode) {
  // create a fifo special file in the current working directory with
  // read-write permissions for communication with the plotter app
  // both proecsses must open the fifo before they perform I/O operations
  // Note: pipe can't be created in a directory shared between 
  // the host OS and VM. Move your code outside the shared directory
  if (mkfifo(pname, 0666) == -1) {
    cout << "Unable to make a fifo. Make sure the pipe does not exist already!" << endl;
    cout << errno << ": " << strerror(errno) << endl << flush;
    exit(-1);
  }

  // opening the fifo for read-only or write-only access
  // a file descriptor that refers to the open file description is
  // returned
  int fd = open(pname, mode);

  if (fd == -1) {
    cout << "Error: failed on opening named pipe." << endl;
    cout << errno << ": " << strerror(errno) << endl << flush;
    exit(-1);
  }

  return fd;
}

// keep in mind that in part 1, the program should only handle 1 request
// in part 2, you need to listen for a new request the moment you are done
// handling one request
int main() {
  WDigraph graph;
  unordered_map<int, Point> points;

  const char *inpipe = "inpipe";
  const char *outpipe = "outpipe";

  // Open the two pipes
  int in = create_and_open_fifo(inpipe, O_RDONLY);
  cout << "inpipe opened..." << endl;
  int out = create_and_open_fifo(outpipe, O_WRONLY);
  cout << "outpipe opened..." << endl;  

  // build the graph
  readGraph("server/edmonton-roads-2.0.1.txt", graph, points);

  // read a request
  // Using new communication protocol to read the data of starting and ending
  // by FIFO
  Point sPoint, ePoint;
  double lat1, lat2, lon1, lon2;
  // create an while loop to keep receive and send massage to plotter.
  while (true) {
    char current[1024];
    read(in, current, 1024);
    string msg(current);
    if(current[0] == 'Q') break;
    sPoint.lat = static_cast<long long>(
      stod(msg.substr(0, msg.find(" ")))*100000);
    msg = msg.substr(msg.find(" ")+1);
    sPoint.lon = static_cast<long long>(
      stod(msg.substr(0, msg.find("\n")))*100000);
    msg = msg.substr(msg.find("\n")+1);
    ePoint.lat = static_cast<long long>(
      stod(msg.substr(0, msg.find(" ")))*100000);
    ePoint.lon = static_cast<long long>(
      stod(msg.substr(msg.find(" ")+1,msg.find("\n")))*100000);
    cout << sPoint.lat << " " << sPoint.lon << endl;
    cout << ePoint.lat << " " << ePoint.lon << endl;

    // get the points closest to the two points we read
    int start = findClosest(sPoint, points), end = findClosest(ePoint, points);

    // run dijkstra's algorithm, this is the unoptimized version that
    // does not stop when the end is reached but it is still fast enough
    unordered_map<int, PIL> tree;
    dijkstra(graph, start, tree);

    // the following program send the shortest path information using communication
    // protocol
    // no path
    if (tree.find(end) == tree.end()) {
      write(out, "E\n", 2);
    }
    else {
      // read off the path by stepping back through the search tree
      list<int> path;
      string result;
      const void* msg_out;
      while (end != start) {
        path.push_front(end);
        end = tree[end].first;
      }
      path.push_front(start);
      for (int v : path) {
        result += to_string(points[v].lat).insert(2,".") + " ";
        result += to_string(points[v].lon).insert(4, ".") + "\n";
      }
      result += "E\n";
      msg_out = static_cast<const void*>(result.c_str());
      write(out, msg_out, result.size());
    }
  }
  close(in);
  close(out);
  unlink(inpipe);
  unlink(outpipe);
  return 0;
}
