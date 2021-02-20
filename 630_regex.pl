open FH, "round2_4s_omitted_tagged.txt";
open FH1, ">relevant.txt";
open FH2, ">irrelevant.txt";
while (<FH>) {
  my $oops;
  while (/_EX.+?VB.+?NN(.+?)(VB\w+|MD)/g) {
    my $str = $1;
    my $vb = $2;
    next if $vb !~ /^(VB|VBZ|VBP|VBD)$/;
    $oops=1 if ($str !~ /NN|PRP|WDT/);
  }
  $oops ? (print FH1 $_) : (print FH2 $_);
}
