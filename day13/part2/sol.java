import java.util.*;
import java.io.*;

class sol {
    private static class Computer {
        private static final Map<Long, Integer> OFFSETS;
        private static final Map<Long, Integer> PARAMS;
        private static final Set<Long> PARAM_WHITELIST;
        private static final int ADDITIONAL_MEM = 5000;
        static {
            OFFSETS = new HashMap<>();
            OFFSETS.put(1L, 4);
            OFFSETS.put(2L, 4);
            OFFSETS.put(3L, 2);
            OFFSETS.put(4L, 2);
            OFFSETS.put(5L, 3);
            OFFSETS.put(6L, 3);
            OFFSETS.put(7L, 4);
            OFFSETS.put(8L, 4);
            OFFSETS.put(9L, 2);
            OFFSETS.put(99L, 1);

            PARAMS = new HashMap<>();
            PARAMS.put(1L, 3);
            PARAMS.put(2L, 3);
            PARAMS.put(3L, 1);
            PARAMS.put(4L, 1);
            PARAMS.put(5L, 2);
            PARAMS.put(6L, 2);
            PARAMS.put(7L, 3);
            PARAMS.put(8L, 3);
            PARAMS.put(9L, 1);
            PARAMS.put(99L, 1);

            PARAM_WHITELIST = new HashSet<>();
            PARAM_WHITELIST.add(1L);
            PARAM_WHITELIST.add(2L);
            PARAM_WHITELIST.add(3L);
            PARAM_WHITELIST.add(4L);
            PARAM_WHITELIST.add(7L);
            PARAM_WHITELIST.add(8L);
        }

        private long[] code;
        private int ptr;
        private int relativeBase;
        private long output;
        private long input;

        public Computer(String[] code) {
            this(code, Long.MIN_VALUE);
        }

        public Computer(String[] code, long initial) {
            this.code = new long[code.length + ADDITIONAL_MEM];
            for (int i = 0; i < code.length; i++) {
                this.code[i] = Long.valueOf(code[i]);
            }
            for (int i = code.length; i < ADDITIONAL_MEM; i++) {
                this.code[i] = 0;
            }
            this.ptr = 0;
            this.relativeBase = 0;
            this.input = initial;
            this.output = Long.MIN_VALUE;
        }

        public long process(long opcode) {
            long opc = opcode % 100;
            long positions = opcode / 100;

            long[] params = new long[3];

            for (int i = 1; i <= Computer.PARAMS.get(opc); i++) {
                long pos = positions % 10;
                if (Computer.PARAM_WHITELIST.contains(opc) && Computer.PARAMS.get(opc).equals(i)) {
                    switch (Long.valueOf(pos).intValue()) {
                    case 0:
                        params[i - 1] = this.code[this.ptr + i];
                        break;
                    case 1:
                        params[i - 1] = this.ptr + i;
                        break;
                    case 2:
                        params[i - 1] = this.code[this.ptr + i] + this.relativeBase;
                        break;
                    }
                } else {
                    switch (Long.valueOf(pos).intValue()) {
                    case 0:
                        params[i - 1] = this.code[(int) this.code[this.ptr + i]];
                        break;
                    case 1:
                        params[i - 1] = this.code[this.ptr + i];
                        break;
                    case 2:
                        params[i - 1] = this.code[(int) this.code[this.ptr + i] + this.relativeBase];
                        break;
                    }
                }
                positions /= 10;
            }

            switch (Long.valueOf(opc).intValue()) {
            case 1:
                this.code[(int) params[2]] = params[0] + params[1];
                break;
            case 2:
                this.code[(int) params[2]] = params[0] * params[1];
                break;
            case 3:
                if (this.input != Long.MIN_VALUE) {
                    this.code[(int) params[0]] = this.input;
                    this.input = Long.MIN_VALUE;
                    break;
                } else {
                    return Long.MIN_VALUE;
                }
            case 4:
                this.ptr += Computer.OFFSETS.get(opc);
                this.output = this.code[(int) params[0]];
                // System.out.print("Output: ");
                // System.out.println(this.code[(int) params[0]]);
                return this.output;
            case 5:
                this.ptr = (params[0] != 0) ? (int) params[1] : this.ptr + Computer.OFFSETS.get(opc);
                return Long.MAX_VALUE;
            case 6:
                this.ptr = (params[0] == 0) ? (int) params[1] : this.ptr + Computer.OFFSETS.get(opc);
                return Long.MAX_VALUE;
            case 7:
                this.code[(int) params[2]] = (params[0] < params[1]) ? 1 : 0;
                break;
            case 8:
                this.code[(int) params[2]] = (params[0] == params[1]) ? 1 : 0;
                break;
            case 9:
                this.relativeBase += params[0];
                break;
            }

            this.ptr += Computer.OFFSETS.get(opc);
            return Long.MAX_VALUE;
        }

        public long crunch() {
            long curr = this.code[this.ptr];

            while (curr != 99) {
                long result = this.process(curr);
                if (result == Long.MIN_VALUE) {
                    break;
                } else if (result != Long.MAX_VALUE) {
                    return result;
                }
                curr = this.code[this.ptr];
            }
            return Long.MIN_VALUE;
        }

        public boolean halted() {
            return this.code[this.ptr] == 99;
        }

        public boolean waiting() {
            return this.code[this.ptr] == 3;
        }

        public Long get() {
            return this.output;
        }

        public void send(int val) {
            this.input = Long.valueOf(val);
        }
    }

    public static void main(String[] args) throws Exception {
        File file = new File("input.txt");

        BufferedReader br = new BufferedReader(new FileReader(file));

        // Read entire file
        int character = br.read();
        StringBuilder intermediate = new StringBuilder();
        while (character != -1) {
            intermediate.append((char) character);
            character = br.read();
        }
        String data = intermediate.toString();
        br.close();

        String[] code = data.split(",");

        code[0] = "2"; // Set to play

        Computer c = new Computer(code);

        int padPos = 0;
        int ballPos = 0;
        int score = 0;

        while (!c.halted()) {
            int x = (int)c.crunch();
            int y = (int)c.crunch();
            int val = (int)c.crunch();
            if (c.waiting()) {
                if (padPos > ballPos) {
                    c.send(-1);
                } else if (ballPos > padPos) {
                    c.send(1);
                } else {
                    c.send(0);
                }
            } else if (x == -1 && y == 0) {
                score = val;
            } else {
                switch ((int)val) {
                    case 0:
                        // Empty tile
                        break;
                    case 1:
                        // Wall tile
                        break;
                    case 2:
                        // Block tile
                        break;
                    case 3:
                        // Horizontal paddle tile
                        padPos = x;
                        break;
                    case 4:
                        // Ball tile
                        ballPos = x;
                        break;
                    default:
                        throw new Exception();
                }
            }
        }

        System.out.print("Final score: ");
        System.out.println(score);
    }
}
