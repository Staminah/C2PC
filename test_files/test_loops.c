int i;
for( i = 0 ; i <= 100 ; i += 1){
    i += 2;
    while (i < 50) {
      i += 3;
      continue;
    }
    break;
}
