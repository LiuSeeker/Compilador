<?php
    $st = "oba";

    echo $st;

    $a = 1;
    if ($a < 5)
        $a =  $a - 10;
    else
        if ($a == 10)
            $a = 20;
        else
            $a = 30;
    
    echo $a;

    $t = true;
    $s = 2;
    
    if(!($s < 0) and $t){
        echo 10000;
        echo "zozo";
    }
    
    if(($a < 0) or ($a == 6) or ($a == 20))
        echo 20000;

    if(($a < 0) and (3 == 4))
        echo 40000;
    
    $b = 0;
    while ($b < 3)
        $b = $b + 1;
    
    echo $b; /*3*/

    $f = 1.true.false."abo".$st;
    echo $f;

    $c = -8/4;
    $d = 3 - $c; 
    $e = 4/ (1+ 1) *2;
    echo $d; /*5*/
    echo $e; /*4*/
?>