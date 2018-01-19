int var = 3;
int toto = var + 7 * 6 -5 / 10;
int zozo = 0;
zozo += 3;
for (zozo = 0; zozo < 100; zozo += 1) {
    if (toto == 7) {
        continue;
    }
    else {
        break;
    }
    toto += 4;
}
