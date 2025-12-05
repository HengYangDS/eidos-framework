SELECT TOP 100 d.TradingDay,
               s.SecuCode,
               d.ClosePrice,
               s.SecuMarket
FROM DZ_DailyQuote d
         JOIN
     SecuMain s ON d.InnerCode = s.InnerCode
WHERE d.TradingDay = '2023-01-04'
