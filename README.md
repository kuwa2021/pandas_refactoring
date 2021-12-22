・フォルダ構成  

    └─pandas_refactoring_test
       │
       ├─data
       │  ├─climate_precip.csv
       │  └─climate_temp.csv
       │
       └─test
          ├─main.py
          └─test_main3.py

main.py  
　・ 9行目のcsvは相対パスで指定している  
　・54行目のdef print_correlations関数ではユニットテストを行うために、corrsというリストを加え条件式を設定できるようにしている