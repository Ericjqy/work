/*
# ---------------------------------------------------
# Name : Qingyun Jia
# ---------------------------------------------------
*/
#include <iostream>
#include <vector>
#include <climits> 
using namespace std;
typedef unsigned int uint;
uint max_len = 0;
/*
Description: get_num_times function is used to find the how much times
	need for the input burst.
Argument: 
    heights: record the given ledges' hight in an array
	length: the total number of ledges
	rest: the time need for resting in ledge
	L: the input burst distance
	num: used to record the total distance had climbbed. At the end, it 
		represent the total time spend.
	wait: the total rest time
	min: the ledge that the people rest and begin his climbing
Return:
    num: represent the total time spend
*/
uint get_num_times(const uint *heights, uint length, uint rest, uint L) {
	uint num = L;
	uint wait = 0;
	uint min = 0;
	// the climbing go through each ledges
	for (uint i=0;i<length;++i) {
		// when next ledge is above the maximum distance we can reach
		if(heights[i]>num){
			// when we rest from last ledge but still can't reach
			if(heights[i]-min>L){
				num = UINT_MAX;
				return num;
				break;
			}
			// we rest from last ledge
			else{
				wait += rest;
				num = heights[i-1] + L;
			}
		}
		min = heights[i];
	}
	num = heights[length-1] + wait;
	return num;
}

/*
Description: climbing is used to find the shortest possible burst by
	binary search
Argument: 
    heights: record the given ledges' hight in an array
	length: the total number of ledges
	rest: the time need for resting in ledge
	limit: the output burst we want
	low: the lower boundary of the possible burst for binary search
	high: the top boundary of possible burst for binary search
Return:
    low+1: at the end, high will equal to low, but since we let high
		be the burst that equal to low, so we let low+1 to get the
		correct value
*/
uint climbing(const uint *heights, uint length, uint rest, uint limit) {
	uint low = 0;
	uint high = max_len;
	// binary search part
	while (low < high) {
		uint mid = (high + low + 1)/2; 
		// when result larger than limit, we want larger burst
		if (get_num_times(heights, length, rest, mid) > limit) {
			low = mid;
		// other wise, we want lower burst
		} else if (get_num_times(heights, length, rest, mid) == limit) {
			high = mid-1;
		} else {
			high = mid-1;
		}
	}
	return low+1;
}

int main() {
    uint length, rest, limit;
    cin >> length >> rest >> limit;
    uint ledge[length];
    for (uint i = 0; i<length; i++){
        cin >> ledge[i];
		if (ledge[i] > max_len)
			max_len = ledge[i];
    }
	cout << climbing(ledge, length, rest, limit) << endl;
	return 0;
}
