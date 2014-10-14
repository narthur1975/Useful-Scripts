RPM=$(<./RPM.txt)

for RPM in $RPM
do 
  CKSUM_VALUE=$(cksum /rpm-repo/cybscm/$RPM | awk '{print $1}')
  echo "$CKSUM_VALUE           $RPM"
done

