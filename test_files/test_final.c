double x = 2.0;
double y = 3.0;

double tests(double x, double y){
  int i = 0;
  double res;

  for (i = 0 ; i < 10 ; i += 1)
  {

    switch(i){
      case 1 :
        res = x+y;
        //printf("%f\n", res);
        res = x-y;
        //printf("%f\n", res);
        res = x*y;
        //printf("%f\n", res);
        res = x/y;
        //printf("%f\n", res);
        res= x%y;
        //printf("%f\n", res);
        break;
      case 2 :
        int j = 1;
        double d = 2.0;
        float f = 3.0f;
        char c = "4";
        const int INT = 5;
        break;
      case 3 :
        while (j < 4) {
          j+=2;
        }
        break;
      default :
        /*if(i <= 4){

        }
        else if (i >= 2){

        }
        else if (i != 5){

        }
        else{

        }*/
    }
  }
}
