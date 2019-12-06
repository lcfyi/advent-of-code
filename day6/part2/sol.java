import java.util.*;
import java.io.*;

class a {

	static Map<String, List<String>> map;
	public static void main(String[] args) throws Exception {
		File file = new File("input.txt");

		BufferedReader br = new BufferedReader(new FileReader(file));

        // Read lines
        List<String> data = new ArrayList<>();
		String line = br.readLine();
		while (line != null) {
			data.add(line);
			line = br.readLine();
        }
		br.close();

		// Construct a map of planet to the other
		map = new HashMap<>();
		
		for (String s : data) {
			String[] splits = s.split("\\)");
			String first = splits[0];
			String second = splits[1];

			map.computeIfAbsent(first, key -> new ArrayList<>()).add(second);
		}

		System.out.println(findShortestPathBetween("COM", "YOU", "SAN"));
	}

	public static long findShortestPathBetween(String start, String first, String second) {
		Queue<String> planets = new LinkedList<>();
		planets.add(start);

		long shortestPath = Long.MAX_VALUE;

		while (!planets.isEmpty()) {
			String currPlanet = planets.remove();
			if (map.containsKey(currPlanet)) {
				for (String p : map.get(currPlanet)) {
					planets.add(p);
				}
			}
			long pathToFirst = findPathLength(currPlanet, first);
			long pathToSecond = findPathLength(currPlanet, second);

			if (pathToFirst == -1 || pathToSecond == -1) {
				continue;
			}

			long path = pathToFirst + pathToSecond;

			if (path < shortestPath) {
				shortestPath = path;
			}
		}

		// Minus 2 to account edges to the elements themselves being counted
		return shortestPath - 2;
	}

	public static long findPathLength(String start, String target) {
		Stack<Long> backtracks = new Stack<>();
		Stack<String> planets = new Stack<>();
		planets.push(start);

		long depth = 0;

		while (!planets.isEmpty()) {
			String currPlanet = planets.pop();
			if (target.equals(currPlanet)) {
				return depth;
			}
			depth++;
			if (map.containsKey(currPlanet)) {
				int count = 0;
				for (String p : map.get(currPlanet)) {
					planets.push(p);
					count++;
					if (count > 1) {
						backtracks.push(depth);
					}
				}
			} else {
				if (backtracks.isEmpty()) {
					return -1;
				}
				depth = backtracks.pop();
			}
			
		}
		return -1;
	}
}
