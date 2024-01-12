server: digraph.o dijkstra.o server.o
	g++ -o server digraph.o dijkstra.o server.o
clean:
	rm -f digraph.o dijkstra.o server.o server

server.o:server.cpp
	g++ -c server.cpp 
digraph.o:digraph.cpp digraph.h
	g++ -c digraph.cpp 
dijkstra.o:dijkstra.cpp dijkstra.h
	g++ -c dijkstra.cpp