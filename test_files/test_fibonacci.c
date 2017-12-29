int n = 3;
int first = 0;
int second = 1;
int next;
int c;

for ( c = 0 ; c < n ; c = c + 1 )
{
    if ( c <= 1 ) {
        next = first + second;
        first = second;
        second = next;
    }
    else {
        next = first + second;
        first = second;
        second = next;
    }
}

return 0;
