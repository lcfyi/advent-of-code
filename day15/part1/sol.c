#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

const long ADDITIONAL_MEM = 5000;

struct Computer
{
    long long *code;
    int ptr;
    int relativeBase;
    long input;
    long long output;
};

int getOffset(long long opcode)
{
    switch ((int)opcode)
    {
    case 1:
        return 4;
    case 2:
        return 4;
    case 3:
        return 2;
    case 4:
        return 2;
    case 5:
        return 3;
    case 6:
        return 3;
    case 7:
        return 4;
    case 8:
        return 4;
    case 9:
        return 2;
    case 99:
        return 1;
    default:
        return INT_MAX; // Fail fast, should segfault
    }
}

int getParamCount(long long opcode)
{
    switch ((int)opcode)
    {
    case 1:
        return 3;
    case 2:
        return 3;
    case 3:
        return 1;
    case 4:
        return 1;
    case 5:
        return 2;
    case 6:
        return 2;
    case 7:
        return 3;
    case 8:
        return 3;
    case 9:
        return 1;
    case 99:
        return 1;
    default:
        return INT_MAX; // Fail fast, should segfault
    }
}

int areParamsWhitelisted(long long opcode)
{
    return opcode == 1 || opcode == 2 || opcode == 3 || opcode == 4 || opcode == 7 || opcode == 8;
}

struct Computer *createComputer(char *code, long length)
{
    struct Computer *c = malloc(sizeof(struct Computer));

    c->ptr = 0;
    c->relativeBase = 0;
    c->input = LLONG_MIN;
    c->output = LLONG_MIN;

    c->code = malloc(sizeof(long long) * (length + ADDITIONAL_MEM));
    int cIdx = 0;

    long start = 0;

    c->code[cIdx] = atoll(&code[0]);
    cIdx++;

    for (int i = 0; i < length; i++)
    {
        if (code[i] == ',')
        {
            c->code[cIdx] = atoll(&code[i + 1]);
            cIdx++;
        }
    }

    for (int i = 0; i < ADDITIONAL_MEM; i++)
    {
        c->code[cIdx] = 0;
        cIdx++;
    }

    return c;
}

// Intermediate function, shouldn't be called directly
long long process(struct Computer *c, long long opcode)
{
    long opc = opcode % 100;
    long positions = opcode / 100;

    long long params[3];

    for (int i = 1; i <= getParamCount(opc); i++)
    {
        long pos = positions % 10;
        if (areParamsWhitelisted(opc) && getParamCount(opc) == i)
        {
            switch (pos)
            {
            case 0:
                params[i - 1] = c->code[c->ptr + i];
                break;
            case 1:
                params[i - 1] = c->ptr + i;
                break;
            case 2:
                params[i - 1] = c->code[c->ptr + i] + c->relativeBase;
                break;
            }
        }
        else
        {
            switch (pos)
            {
            case 0:
                params[i - 1] = c->code[c->code[c->ptr + i]];
                break;
            case 1:
                params[i - 1] = c->code[c->ptr + i];
                break;
            case 2:
                params[i - 1] = c->code[c->code[c->ptr + i] + c->relativeBase];
                break;
            }
        }
        positions /= 10;
    }

    switch (opc)
    {
    case 1:
        c->code[params[2]] = params[0] + params[1];
        break;
    case 2:
        c->code[params[2]] = params[0] * params[1];
        break;
    case 3:
        if (c->input != LLONG_MIN)
        {
            c->code[params[0]] = c->input;
            c->input = LLONG_MIN;
            break;
        }
        else
        {
            return LLONG_MIN;
        }
    case 4:
        c->ptr += getOffset(opc);
        c->output = c->code[params[0]];
        // printf("Output: %lld\n", c->output);
        return c->output;
    case 5:
        c->ptr = (params[0] != 0) ? params[1] : c->ptr + getOffset(opc);
        return LLONG_MAX;
    case 6:
        c->ptr = (params[0] == 0) ? params[1] : c->ptr + getOffset(opc);
        return LLONG_MAX;
    case 7:
        c->code[params[2]] = (params[0] < params[1]) ? 1 : 0;
        break;
    case 8:
        c->code[params[2]] = (params[0] == params[1]) ? 1 : 0;
        break;
    case 9:
        c->relativeBase += params[0];
        break;
    }

    c->ptr += getOffset(opc);
    return LLONG_MAX;
}

long long crunch(struct Computer *c)
{
    long long curr = c->code[c->ptr];

    while (curr != 99)
    {
        long long result = process(c, curr);
        if (result == LLONG_MIN)
        {
            break;
        }
        else if (result != LLONG_MAX)
        {
            return result;
        }
        curr = c->code[c->ptr];
    }

    return LLONG_MIN;
}

int halted(struct Computer *c)
{
    return c->code[c->ptr] == 99;
}

const int HEIGHT = 50;
const int WIDTH = 50;

// Literally the most brute force solution I've come up with yet
void generateMaze(char map[WIDTH][HEIGHT], char *data, long length)
{
    struct Computer *c = createComputer(data, length);

    int dir = 0;
    int x = WIDTH / 2;
    int y = HEIGHT / 2;

    int iter = 0;

    while (1)
    {
        dir = rand() % 4 + 1;
        c->input = dir;
        switch (dir)
        {
        case 1: // North
            y--;
            break;
        case 2: // South
            y++;
            break;
        case 3: // West
            x--;
            break;
        case 4: // East
            x++;
            break;
        }
        long long res = crunch(c);
        switch (res)
        {
        case 0:
            // Hit a wall
            map[x][y] = '#';
            // Reverse the dir
            switch (dir)
            {
            case 1: // North
                y++;
                break;
            case 2: // South
                y--;
                break;
            case 3: // West
                x++;
                break;
            case 4: // East
                x--;
                break;
            }
            break;
        case 1:
            // Moved in the dir, track that we've written something
            switch (dir)
            {
            case 1: // North
                map[x][y + 1] = '.';
                break;
            case 2: // South
                map[x][y - 1] = '.';
                break;
            case 3: // West
                map[x + 1][y] = '.';
                break;
            case 4: // East
                map[x - 1][y] = '.';
                break;
            }
            break;
        case 2:
            // Moved in the dir, found the oxygen system
            map[x][y] = 'O';
            c = createComputer(data, length);
            x = WIDTH / 2;
            y = HEIGHT / 2;
            iter++;
            map[HEIGHT / 2][WIDTH / 2] = 'X';
            if (iter == 5)
                return;
            break;
        default:
            return;
        }
    }
}

int min(int a, int b)
{
    if (a < b)
        return a;
    else
        return b;
}

int max(int a, int b)
{
    if (a < b)
        return b;
    else
        return a;
}

int getShortestPath(char seen[WIDTH][HEIGHT], char map[WIDTH][HEIGHT], int depth, int x, int y)
{
    if (map[x][y] == '#' || map[x][y] == ' ')
    {
        return INT_MAX;
    }
    if (map[x][y] == 'O')
    {
        printf("other depth %d\n", depth);
        return depth;
    }

    // Mark as seen
    seen[x][y] = '.';

    int L;
    int R;
    int U;
    int D;

    if (seen[x - 1][y] == ' ')
        L = getShortestPath(seen, map, depth + 1, x - 1, y);
    else
        L = INT_MAX;
    if (seen[x + 1][y] == ' ')
        R = getShortestPath(seen, map, depth + 1, x + 1, y);
    else
        R = INT_MAX;
    if (seen[x][y - 1] == ' ')
        U = getShortestPath(seen, map, depth + 1, x, y - 1);
    else
        U = INT_MAX;
    if (seen[x][y + 1] == ' ')
        D = getShortestPath(seen, map, depth + 1, x, y + 1);
    else
        D = INT_MAX;

    return min(L, min(R, min(U, D)));
}

int main(void)
{
    FILE *file;

    file = fopen("input.txt", "r");

    // Read entire file
    char *data = 0;
    long length = 0;
    if (file)
    {
        fseek(file, 0, SEEK_END);
        length = ftell(file);
        fseek(file, 0, SEEK_SET);
        data = malloc(length);

        if (data)
        {
            fread(data, 1, length, file);
        }

        fclose(file);
    }

    char map[WIDTH][HEIGHT];
    char seen[WIDTH][HEIGHT];

    for (int x = 0; x < WIDTH; x++)
    {
        for (int y = 0; y < HEIGHT; y++)
        {
            map[x][y] = ' ';
            seen[x][y] = ' ';
        }
    }

    generateMaze(map, data, length);

    int x = WIDTH / 2;
    int y = HEIGHT / 2;

    int p = getShortestPath(seen, map, 0, x, y);

    printf("Depth: %d\n", p);

    return 0;
}