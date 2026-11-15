/* enum_profiles.cpp -- Q2: exhaustive enumeration of level profiles of position product events without gains.
   Written from the definitions (draft subsection, proof of thm:tp: the unrolled lattice) alone.

   MODEL. State after t masks: n: Z -> N, n(e) = number of walks of the event with e left steps ("deficit").
   n_0 = delta_0.  A mask is a set E of residues mod M (site t-2e mod N <-> e mod M, a bijection onto the sites
   reachable at time t).  n_t(e) = [e mod M in E_t] (n_{t-1}(e) + n_{t-1}(e-1)).
   Profile at a site of an event of length T (T>=1): for a residue c, u_j = n_{T-1}(c+jM) (rail R),
   v_j = n_{T-1}(c-1+jM) (rail L); w = (v_0,u_0,v_1,u_1,...) with j shifted so that the first non-zero entry
   has index 0 or 1.  Convention: l0 = least lambda on either rail, so w_0 = v_0 counts L-walks with lambda=l0.

   BOUNDS (arguments: M B K [maxstates]).  B: total of the profile (u(1)+v(1)) at most B.  K: at most K levels j.
   Search is over ALL sequences of masks of ALL lengths (breadth first to closure) whose states satisfy
     (a) every residue class of n_t has total <= B,  (b) support of n_t has max e - min e <= (K+1)M.
   Claim proved in the coordinator's notes (not by this program): (a),(b) lose no profile with total <= B and
   <= K levels, because the classes that do not reach the site can be masked out ("trim").
   States are stored exactly (4 bits per entry, B <= 15, (K+1)M+1 <= 48), up to translation of e.

   PREDICATES (fixed before the first run; evaluated by compare_profiles.py, which reads this program's output):
   P0 control: allowed sets reproduce the draft's counts 550 (<=4 levels, total<=9) and 228 (total<=7).
   P1 necessity: every profile seen is allowed (thm:tp / cor:tp(iii)).  Hypothesis: profile comes from an event (always true here; counted).
   P2 sufficiency within bounds: every allowed profile (total<=B, <=K levels) is seen.  Failures are kept, per M.
   P3 the root criterion of cor:tp(iii) agrees with minors of the array (see compare_profiles.py).
   Result files are never overwritten (program refuses).  No randomness: no seed is used.
*/
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
struct Key{u64 a[3]; bool operator==(const Key&o)const{return a[0]==o.a[0]&&a[1]==o.a[1]&&a[2]==o.a[2];}};
static inline u64 hk(const Key&k){u64 h=k.a[0]*0x9E3779B97F4A7C15ULL; h^=h>>29; h+=k.a[1]*0xC2B2AE3D27D4EB4FULL; h^=h>>31; h+=k.a[2]*0x165667B19E3779F9ULL; h^=h>>32; h*=0xD6E8FEB86659FD93ULL; h^=h>>32; return h;}
struct HSet{ vector<Key> t; size_t n=0, cap; HSet(size_t c=1<<26):t(c,Key{{0,0,0}}),cap(c){}
  bool ins(const Key&k){ if(10*(n+1)>7*cap) grow(); size_t i=hk(k)&(cap-1); while(true){ Key&s=t[i]; if(s.a[0]==0&&s.a[1]==0&&s.a[2]==0){s=k;n++;return true;} if(s==k) return false; i=(i+1)&(cap-1);} }
  void grow(){ vector<Key> o; o.swap(t); cap*=2; t.assign(cap,Key{{0,0,0}}); n=0; for(auto&k:o) if(k.a[0]|k.a[1]|k.a[2]) ins(k);} };
int M,B,K,L;
static inline Key pack(const unsigned char*n){Key k{{0,0,0}}; for(int e=0;e<L;e++) k.a[e>>4]|=(u64)n[e]<<(4*(e&15)); return k;}
static inline void unpack(const Key&k,unsigned char*n){for(int e=0;e<L;e++) n[e]=(k.a[e>>4]>>(4*(e&15)))&15;}
set<vector<int>> seen;
void record(const unsigned char*n){
  for(int c=0;c<M;c++){
    vector<int> w; int tot=0;
    for(int j=0;;j++){ int e1=c-1+j*M,e2=c+j*M; if(e1>=L&&e2>=L)break; int a=(e1>=0&&e1<L)?n[e1]:0,b=(e2<L)?n[e2]:0; w.push_back(a);w.push_back(b);tot+=a+b;}
    if(tot==0||tot>B) continue;
    size_t i0=0; while(w[i0]==0)i0++; i0=2*(i0/2); w.erase(w.begin(),w.begin()+i0); while(w.back()==0)w.pop_back();
    if((int)(w.size()+1)/2>K) continue;
    seen.insert(w);
  }
}
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: M B K [maxstates]\n");return 2;}
  M=atoi(argv[1]);B=atoi(argv[2]);K=atoi(argv[3]); size_t maxst=argc>4?strtoull(argv[4],0,10):44000000ULL;
  L=(K+1)*M+1; if(L>48||B>15||M<3){fprintf(stderr,"bounds not representable\n");return 2;}
  char fn[200]; snprintf(fn,200,"seen_M%d_B%d_K%d.txt",M,B,K);
  if(FILE*f=fopen(fn,"r")){fclose(f);fprintf(stderr,"refuse to overwrite %s\n",fn);return 3;}
  HSet vis; vector<Key> fr,nx; unsigned char n[64],m[64];
  memset(n,0,sizeof n); n[0]=1; Key k0=pack(n); vis.ins(k0); fr.push_back(k0); record(n);
  u64 pr_tot=0,pr_span=0,trans=0; int layer=0; bool closed=false; vector<size_t> layers;
  while(true){
    layers.push_back(fr.size()); nx.clear();
    for(const Key&k:fr){
      unpack(k,n); n[L]=0; int occ=0; for(int e=0;e<L;e++) if(n[e]) occ|=1<<(e%M);
      int cand=occ|((occ<<1)&((1<<M)-1))|(occ>>(M-1));
      for(int E=cand;E>0;E=(E-1)&cand){
        trans++; int ct[16]={0}; bool bad=false; int first=-1,last=-1;
        for(int e=0;e<=L;e++){ int r=e%M; int val=0; if(E>>r&1){ val=(e<L?n[e]:0)+(e>0?n[e-1]:0); if(val){ ct[r]+=val; if(ct[r]>B){bad=true;break;} if(first<0)first=e; last=e; } } m[e]=val; }
        if(bad){pr_tot++;continue;} if(first<0)continue;
        if(last-first>(K+1)*M){pr_span++;continue;}
        unsigned char q[64]; memset(q,0,sizeof q); for(int e=first;e<=last;e++) q[e-first]=m[e];
        /* residues are relative to the first occupied entry; shift by `first` relabels them consistently */
        Key kk=pack(q); if(vis.ins(kk)){ nx.push_back(kk); record(q);} 
      }
    }
    layer++;
    if(nx.empty()){closed=true;break;}
    if(vis.n>maxst){break;}
    fr.swap(nx);
  }
  FILE*f=fopen(fn,"w");
  fprintf(f,"# M=%d B=%d K=%d states=%zu layers=%d closed=%d transitions=%llu pruned_total=%llu pruned_span=%llu profiles=%zu\n",M,B,K,vis.n,layer,(int)closed,trans,pr_tot,pr_span,seen.size());
  fprintf(f,"# layer sizes:"); for(size_t s:layers)fprintf(f," %zu",s); fprintf(f,"\n");
  for(auto&w:seen){ for(size_t i=0;i<w.size();i++)fprintf(f,"%s%d",i?" ":"",w[i]); fprintf(f,"\n"); }
  fclose(f);
  printf("M=%d B=%d K=%d states=%zu layers=%d closed=%d profiles=%zu\n",M,B,K,vis.n,layer,(int)closed,seen.size());
  return closed?0:4;
}
