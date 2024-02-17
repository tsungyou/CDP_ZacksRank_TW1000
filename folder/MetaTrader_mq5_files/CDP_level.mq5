// Simply using loop for drawing linesr4

#property copyright "Jimmy Lee"
#property link      "https://www.mql5.com"
#property version   "1.00"
input color input_hline_color = clrWhite;
input int input_hline_width = 3;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   double value_array[];
   double high = NormalizeDouble(iHigh(_Symbol, PERIOD_D1, 1), _Digits);
   double low = NormalizeDouble(iLow(_Symbol, PERIOD_D1, 1), _Digits);
   double open = NormalizeDouble(iOpen(_Symbol, PERIOD_D1, 1), _Digits);
   double close = NormalizeDouble(iClose(_Symbol, PERIOD_D1, 1), _Digits);
   double CDP = NormalizeDouble((open + high+ low + close)/4, _Digits);
   double AH = CDP + (high - low);
   double NH = 2*CDP - low;
   double NL = 2*CDP - high;
   double AL = CDP - (high - low);
   double array[5] = {CDP, AH, NH, NL, AL};
   string array_name[5] = {"CDP", "AH", "NH", "NL", "AL"};
   datetime time_current = iTime(_Symbol, PERIOD_D1, 0);
   datetime time_past = iTime(_Symbol, PERIOD_D1, 2);
   
   for(int i=0; i<5; i++)
   {
      ObjectCreate(0, array_name[i],  OBJ_HLINE, 0, time_past, array[i], time_current, array[i]);
      ObjectSetInteger(0, array_name[i], OBJPROP_COLOR, input_hline_color);
      ObjectSetInteger(0, array_name[i], OBJPROP_WIDTH, input_hline_width);
   }

  }
//+------------------------------------------------------------------+