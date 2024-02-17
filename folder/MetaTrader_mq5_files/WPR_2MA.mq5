
#property copyright "Jimmy Lee"
#property link      "https://www.mql5.com/zh/articles/12599"
#property version   "1.00"
#include <Trade/Trade.mqh>
#include <Trade/PositionInfo.mqh>
input int cal_period_wpr = 14;
input int short_ma = 14;
input int long_ma = 28;

CTrade trade;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   const ulong magic_number = 123456;
   trade.SetExpertMagicNumber(magic_number);
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


   double ma1[];
   double ma2[];
   int moving1 = iMA(_Symbol, PERIOD_CURRENT, short_ma, 0, MODE_EMA, PRICE_CLOSE);
   int moving2 = iMA(_Symbol, PERIOD_CURRENT, long_ma, 0, MODE_EMA, PRICE_CLOSE);
   ArraySetAsSeries(ma1, true);
   ArraySetAsSeries(ma2, true);
   CopyBuffer(moving1, 0, 0, 3, ma1);
   CopyBuffer(moving2, 0, 0, 3, ma2);
   
   double short_0 = ma1[0];
   double short_1 = ma1[1];
   double long_0 = ma2[0];
   double long_1 = ma2[1];
   
   double wprarray[];
   ArraySetAsSeries(wprarray, true);
   int wpr = iWPR(_Symbol, PERIOD_CURRENT, cal_period_wpr);
   CopyBuffer(wpr, 0, 0, 2, wprarray);
   
   
   
   double wpvalue0 = NormalizeDouble(wprarray[0], 2);
   double wpvalue1 = NormalizeDouble(wprarray[1], 2);
   Comment("Williams %R Value is", wpvalue0, " Williams %R Value1 is", wpvalue1);
   double bid = NormalizeDouble(SymbolInfoDouble(_Symbol, SYMBOL_BID), _Digits);
   double ask = NormalizeDouble(SymbolInfoDouble(_Symbol, SYMBOL_ASK), _Digits);
   double sl = NormalizeDouble(ask*0.9, 2);
   double tp = NormalizeDouble(ask*1.2, 2);
   double sl_sell = NormalizeDouble(bid*1.1, 2);
   double tp_sell = NormalizeDouble(bid*0.8, 2);
   
   //int position_type_or_even_not_exist = PositionExists();
   
   if((short_0 > long_0) && (wpvalue1 < -80 && wpvalue0 > -80) && !PositionSelect(_Symbol))
   {
      trade.Buy(10, _Symbol, bid, sl, tp, "buy stock");
      Comment("buy symbol");
   }
   else if((short_0 < long_0) && (wpvalue1 > -20 && wpvalue0 < -20) && !PositionSelect(_Symbol))
   {
      trade.Sell(10, _Symbol, ask, sl_sell, tp_sell, "sell stock");
      Comment("Sell");
   }
}
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+

int PositionExists() {   
   if(PositionSelect(_Symbol)){
      if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) return 1;
      if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL) return 2;
   }
   else{
      return 0;
   }
   return 0;
}
