import java.util.*;
import java.io.*;

class sol {

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

        System.out.println(count("COM", 0));
    }

    public static long count(String planet, long depth) {
        if (!map.containsKey(planet)) {
            return depth;
        }
        long c = 0;
        for (String p : map.get(planet)) {
            c += count(p, depth + 1);
        }
        return depth + c;
    }
}
