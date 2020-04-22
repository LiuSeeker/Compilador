{
    $a = readline();
    if ($a < 5)
        $a =  $a - 10;
    else
        $a =  $a + 10;
    
    echo $a;
    
    if(!($a < 0) and (3 == 3))
        echo 10000;
    
    if(($a < 0) or ($a == 6) or ($a == 20))
        echo 20000;

    if(($a < 0) and (3 == 4))
        echo 40000;
    
    $b = 0;
    while ($b < 3)
        $b = $b + 1;
    
    echo $b; /*3*/

    $c = -8/4;
    $d = 3 - $c; 
    {
        $e = 4/ (1+ 1) *2;
    }
    echo $d; /*5*/
    echo $e; /*4*/
}