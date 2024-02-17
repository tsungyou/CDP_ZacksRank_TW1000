//+------------------------------------------------------------------+
//|                                                   TrailingCT.mqh |
//|                   Copyright 2009-2013, MetaQuotes Software Corp. |
//|                                              http://www.mql5.com |
//+------------------------------------------------------------------+
#include <Math\Alglib\fasttransforms.mqh>
#include <Expert\ExpertTrailing.mqh>
// wizard description start
//+------------------------------------------------------------------+
//| Description of the class                                         |
//| Title=Trailing Stop based on 'Fourier Transform' v1              |
//| Type=Trailing                                                    |
//| Name=CategoryTheory                                              |
//| ShortName=CT                                                     |
//| Class=CTrailingFT                                                |
//| Page=trailing_ct                                                 |
//| Parameter=Points,int,6,FT-Points                                 |
//| Parameter=Epicycles,int,5,FT-Epicycles                           | 
//| Parameter=Step,double,0.5,Trailing Step                          |
//| Parameter=Index,int,0,FT-Index                                   |
//+------------------------------------------------------------------+
// wizard description end
//+------------------------------------------------------------------+
//| Class CTrailingFT.                                               |
//| Appointment: Class traling stops with 'Fourier Transform' v1     |
//|               relative-sets concepts.                            |
//| Derives from class CExpertTrailing.                              |
//+------------------------------------------------------------------+
#define     __PI 245850922/78256779

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class CTrailingFT : public CExpertTrailing
  {
protected:
   CFastFourierTransform   FFT;
   
   //--- adjusted parameters
   
   double            m_step;                    // trailing step

   int               m_index;                    // the epicycle index

public:
   //--- methods of setting adjustable parameters
   
   
   
   //--- method of verification of settings
   virtual bool      ValidationSettings(void);
   //--- method of creating the indicator and timeseries
   virtual bool      InitIndicators(CIndicators *indicators);
   //--- methods of checking if the market models are formed
   virtual bool      CheckTrailingStopLong(CPositionInfo *position,double &sl,double &tp);
   virtual bool      CheckTrailingStopShort(CPositionInfo *position,double &sl,double &tp);
   //---
                     CTrailingFT(void);
                    ~CTrailingFT(void);
   //--- methods of setting adjustable parameters
   void              Step(double value)                  { m_step=value;      }
   void              Index(int value)                    { m_index=value;     }

protected:
   
   double            ProcessFT(int Index);

  };
//+------------------------------------------------------------------+
//| Constructor                                                      |
//+------------------------------------------------------------------+
CTrailingFT::CTrailingFT(void)
  {
//--- initialization of protected data
   m_used_series=USE_SERIES_TIME+USE_SERIES_SPREAD+USE_SERIES_OPEN+USE_SERIES_HIGH+USE_SERIES_LOW+USE_SERIES_CLOSE;
  }
//+------------------------------------------------------------------+
//| Destructor                                                       |
//+------------------------------------------------------------------+
CTrailingFT::~CTrailingFT(void)
  {
  }
//+------------------------------------------------------------------+
//| Validation settings protected data.                              |
//+------------------------------------------------------------------+
bool CTrailingFT::ValidationSettings(void)
  {
//--- validation settings of additional filters
   if(!CExpertTrailing::ValidationSettings())
      return(false);
//--- initial data checks
   if(m_index<0 || m_index>=5)
     {
      printf(__FUNCTION__+": index must be greater than 0 and less than epicycles");
      return(false);
     }

//--- ok
   return(true);
  }
//+------------------------------------------------------------------+
//| Create indicators.                                               |
//+------------------------------------------------------------------+
bool CTrailingFT::InitIndicators(CIndicators *indicators)
  {
//--- check pointer
   if(indicators==NULL)
      return(false);
//--- initialization of indicators and timeseries of additional filters
   if(!CExpertTrailing::InitIndicators(indicators))
      return(false);
//--- 
//--- ok
   return(true);
  }
//+------------------------------------------------------------------+
//| Checking trailing stop and/or profit for long position.          |
//+------------------------------------------------------------------+
bool CTrailingFT::CheckTrailingStopLong(CPositionInfo *position,double &sl,double &tp)
  {
//--- check
      if(position==NULL)
         return(false);
      
      m_high.Refresh(-1);
      m_low.Refresh(-1);
      
      int _x=StartIndex();
      
      double _ft=ProcessFT(_x);
      double _type=_ft/100.0;
      
      double _atr=fmax(2.0*m_spread.GetData(_x)*m_symbol.Point(),m_high.GetData(_x)-m_low.GetData(_x))*(_type);
      
      double _sl=m_low.GetData(_x)-(m_step*_atr);
      
      double level =NormalizeDouble(m_symbol.Bid()-m_symbol.StopsLevel()*m_symbol.Point(),m_symbol.Digits());
      double new_sl=NormalizeDouble(_sl,m_symbol.Digits());
      double pos_sl=position.StopLoss();
      double base  =(pos_sl==0.0) ? position.PriceOpen() : pos_sl;
      
      sl=EMPTY_VALUE;
      tp=EMPTY_VALUE;
      if(new_sl>base && new_sl<level)
         sl=new_sl;
//---
   return(sl!=EMPTY_VALUE);
  }
//+------------------------------------------------------------------+
//| Checking trailing stop and/or profit for short position.         |
//+------------------------------------------------------------------+
bool CTrailingFT::CheckTrailingStopShort(CPositionInfo *position,double &sl,double &tp)
  {
//--- check
      if(position==NULL)
         return(false);
   
      m_high.Refresh(-1);
      m_low.Refresh(-1);
      
      int _x=StartIndex();
      
      double _ft=ProcessFT(_x);
      double _type=_ft/100.0;
   
      double _atr=fmax(2.0*m_spread.GetData(_x)*m_symbol.Point(),m_high.GetData(_x)-m_low.GetData(_x))*(_type);
      
      double _sl=m_high.GetData(_x)+(m_step*_atr);
      
      double level =NormalizeDouble(m_symbol.Ask()+m_symbol.StopsLevel()*m_symbol.Point(),m_symbol.Digits());
      double new_sl=NormalizeDouble(_sl,m_symbol.Digits());
      double pos_sl=position.StopLoss();
      double base  =(pos_sl==0.0) ? position.PriceOpen() : pos_sl;
      
      sl=EMPTY_VALUE;
      tp=EMPTY_VALUE;
      if(new_sl<base && new_sl>level)
         sl=new_sl;
//---
      return(sl!=EMPTY_VALUE);
  }
//+------------------------------------------------------------------+
//| Fourier Transform                                                |
//| INPUT PARAMETERS                                                 |
//|     Index   -   int, read index within price buffer.             |
//| OUTPUT                                                           |
//|     double  -   forecast change in price                         |
//+------------------------------------------------------------------+
double CTrailingFT::ProcessFT(int Index)
   {
      double _ft=0.0;
      
      int _index=Index;//+StartIndex();
      
      m_close.Refresh(-1);
      
      double _a[];
      matrix _output;
      al_complex _f[];
      
      //6 data points, 5 epicycles
   
      ArrayResize(_a,6);ArrayInitialize(_a,0.0);
      _output.Init(6,5);_output.Fill(0.0);
      
      for(int p=0;p<6;p++)
      {
         _a[p]=m_close.GetData(_index+p)-m_close.GetData(_index+p+1);
      }
      
      FFT.FFTR1D(_a,5,_f);
       
      for(int p=0;p<6;p++)
      {
         for(int s=0;s<5;s++)
         {
            double _divisor=(1.0/5),_angle=(p);_angle/=6;
            _output[p][s]=(_divisor*_a[p]*MathExp(-2.0*__PI*(_f[s].im/_f[s].re)*_angle));
         }
      }
      
      double _close=m_close.GetData(_index)>m_close.GetData(_index+1);
      
      _ft=(_output[5][m_index]/fmax(m_symbol.Point(),fabs(_output[5][m_index])+fabs(_close)))*100.0;
      
      return(_ft);
   }
//+------------------------------------------------------------------+
