import java.util.*;
import java.io.*;

class sol {
    private static class Pair {
        private final Integer left;
        private final Integer right;

        public Pair(Integer left, Integer right) {
            this.left = left;
            this.right = right;
        }

        @Override
        public String toString() {
            return this.left.toString() + " " + this.right.toString();
        }

        @Override
        public int hashCode() {
            return left.hashCode() ^ right.hashCode();
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof Pair))
                return false;
            Pair other = (Pair) o;
            return this.left.equals(other.left) && this.right.equals(other.right);
        }
    }

    static List<List<Character>> asteroidField;

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

        // Continue to parse lines
        asteroidField = new ArrayList<>();

        for (int i = 0; i < data.size(); i++) {
            for (Character c : data.get(i).toCharArray()) {
                if (asteroidField.size() == i) {
                    asteroidField.add(new ArrayList<>());
                }
                asteroidField.get(i).add(c);
            }
        }
        int max = 0;
        
        for (int y = 0; y < asteroidField.size(); y++) {
            for (int x = 0; x < asteroidField.get(0).size(); x++) {
                if (asteroidField.get(y).get(x).equals('#')) {
                    int currCount = getAsteroidsDetected(x, y);
                    if (currCount > max) {
                        max = currCount;
                    }
                }
            }
        }

        System.out.println(max);
    }

    public static int getAsteroidsDetected(int x, int y) {
        // Make a set of x,y offsets that we've seen, if the asteroid we're 
        // interested in is in that set, then we don't add the count. Otherwise we do
        Set<Pair> pairs = new HashSet<>();
        Set<Pair> seen = new HashSet<>();

        Queue<Pair> todo = new LinkedList<>();

        todo.add(new Pair(x, y));
        seen.add(new Pair(x, y));

        int count = 0;
        
        while (!todo.isEmpty()) {
            Pair currCord = todo.remove();
            int curX = currCord.left;
            int curY = currCord.right;

            int offX = x - curX;
            int offY = y - curY;
            int gcf = getGCF(offX, offY);
            Pair normalized = new Pair(offX / gcf, offY / gcf);
            if (normalized.left == 0 && normalized.right != 0) {
                normalized = new Pair(0, normalized.right / Math.abs(normalized.right));
            }
            if (normalized.right == 0 && normalized.left != 0) {
                normalized = new Pair(normalized.left / Math.abs(normalized.left), 0);
            }

            if (asteroidField.get(curY).get(curX).equals('#') 
                && verifyNoBlocking(normalized, pairs)) {
                pairs.add(normalized);
                count++;
            }

            List<Pair> candidates = new ArrayList<>();
            candidates.add(new Pair(curX + 1, curY - 1));
            candidates.add(new Pair(curX, curY - 1));
            candidates.add(new Pair(curX - 1, curY - 1));
            candidates.add(new Pair(curX - 1, curY));
            candidates.add(new Pair(curX - 1, curY + 1));
            candidates.add(new Pair(curX, curY + 1));
            candidates.add(new Pair(curX + 1, curY + 1));
            candidates.add(new Pair(curX + 1, curY));

            for (Pair p : candidates) {
                if (verifyBounds(p) && !seen.contains(p)) {
                    todo.add(p);
                    seen.add(p);
                }
            }
        }

        return count;
    }

    public static boolean verifyBounds(Pair curr) {
        return curr.left >= 0 && curr.right >= 0 && curr.left < asteroidField.get(0).size()
                && curr.right < asteroidField.size();
    }

    public static int getGCF(int a, int b) {
        a = Math.abs(a);
        b = Math.abs(b);
        int min = b;
        if (a < b) {
            min = a;
        }

        int gcf = 1;
        for (int i = 1; i <= min; i++) {
            if (a % i == 0 && b % i == 0) {
                gcf = i;
            }
        }
        
        return gcf;
    }

    public static boolean verifyNoBlocking(Pair curr, Set<Pair> pairs) {
        if (curr.left == 0 && curr.right == 0) {
            return false;
        }
        return !pairs.contains(curr);
    }
}
