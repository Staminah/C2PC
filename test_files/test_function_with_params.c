int lel(int a)
{
    a = 8;
    return a;
}

int kek(int a, int b)
{
    a = 9;
    b = lel(a);
    return a*b;
}

int x;
x = 2;
double z = 6.5;

int y;
y = kek(x, z);
x = 7;
