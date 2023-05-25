C1_file = climbing.cpp
output = we7_solution
we7_solution: climbing.o
	g++ climbing.o -o $(output)

climbing.o: $(C1_file)
	g++ -c $(C1_file)

clean:
	rm *.o $(output)
