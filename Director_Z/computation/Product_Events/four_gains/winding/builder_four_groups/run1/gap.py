import sys; sys.argv=['x','11','3','2','/dev/null']
exec(open('exact_bfs.py').read().split('# hypothesis test')[0].replace("out=open(sys.argv[4],'x')",""))
for M in (3,4,5):
  for k in (4,6,8):
    seen,prof=search(M,k*M)
    def mg(n):
        occ=[p for p,c in enumerate(n) if c]; return max([b-a for a,b in zip(occ,occ[1:])]+[0])
    print(M,k*M,len(seen),len(prof),'maxwidth',max(len(n) for n in seen),'maxgap',max(mg(n) for n in seen))
