"""Render the velocity-bin and reflected-window model probabilities."""
from argparse import ArgumentParser
from fractions import Fraction
import json
from math import isclose
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, PercentFormatter

from check_velocity_readout import velocity_cdf


def plot(data, output):
    bins = 32
    edges = [-1+2*k/bins for k in range(bins+1)]
    mass = [velocity_cdf(b)-velocity_cdf(a) for a,b in zip(edges,edges[1:])]
    reference = next(row["statistics"] for row in data["after_inner_limit"] if row["bins"]==bins)
    fig, (velocity, window) = plt.subplots(1,2,figsize=(11.7,4.8))
    fig.subplots_adjust(left=.074,right=.982,bottom=.17,top=.77,wspace=.29)
    fig.suptitle("How the detector weights a walk", x=.026, y=.98, ha="left",
                 fontsize=18, fontweight="bold", color="#172833")
    blue, red, gold, green = "#17547B", "#AD462C", "#84631A", "#25755F"
    for ax in (velocity,window):
        ax.set_axisbelow(True)
        ax.grid(axis="y",color="#D9DCDB",linewidth=.7)
        ax.spines[["top","right"]].set_visible(False)
        ax.spines[["left","bottom"]].set_color("#849399")
        ax.tick_params(length=3,color="#849399",labelsize=9)
        ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
    velocity.set_title("Velocity after a free flight",loc="left",pad=27,fontweight="bold")
    velocity.text(0,1.027,"32 equal bins, after the long-time limit",transform=velocity.transAxes,
                  fontsize=9,color="#425761")
    for q,color,line in [(0,"#696974",":"),(.5,gold,"--"),(1,blue,"-"),(2,red,"-.")]:
        score = [1]*bins if q==0 else [b**q for b in mass]
        weights = [x/sum(score) for x in score]
        assert isclose(sum(weights[bins//2:]),reference[str(q)]["positive_velocity"])
        assert isclose(sum(weights[3*bins//8:5*bins//8]),reference[str(q)]["central_quarter"])
        velocity.stairs(weights,edges,baseline=None,linewidth=1.9,color=color,
                        linestyle=line,label=f"$q={q:g}$")
    velocity.set_xlim(-1,1)
    velocity.set_ylim(bottom=-.012)
    velocity.set_xticks([-1,-.5,0,.5,1])
    velocity.set_xlabel("Displacement / ticks")
    velocity.set_ylabel("Probability per velocity bin")
    velocity.legend(loc="upper left",ncol=2,frameon=False,fontsize=9)
    window.set_title("Final position in a window",loc="left",pad=27,fontweight="bold")
    window.text(0,1.027,"Reflecting interval, final normalized position between 3/16 and 5/16",
                transform=window.transAxes,fontsize=8.7,color="#425761")
    p = velocity_cdf(-5/12)-velocity_cdf(-7/12)+velocity_cdf(1/4)-velocity_cdf(1/12)
    rows = data["all_clocks"]
    x = list(range(len(rows)))
    limitx = x[-1]+1.65
    for q,key,label,color,marker,asymptote in [
            ("1","power_then_pool","Ordinary",blue,"o",p),
            ("2","power_then_pool","Square each site",red,"s",0),
            ("2","pool_then_power","Pool window, then square",green,"^",p*p/(p*p+(1-p)**2))]:
        y = []
        for row in rows:
            item = row["powers"][q][key]
            value = float(Fraction(int(item["numerator_hex"],16),int(item["denominator_hex"],16)))
            assert isclose(value,item["ratio"])
            y.append(value)
        assert rows[0]["tick"]==6 and y[0]==0
        window.plot(x,y,label=label,color=color,marker=marker,markersize=4,linewidth=1.5)
        window.scatter([limitx],[asymptote],facecolors="white",edgecolors=color,
                       linewidths=1.6,marker=marker,s=34,zorder=5)
    window.axvline((x[-1]+limitx)/2,color="#A1AAAC",linewidth=.7,linestyle=":")
    ticks = x[::2]+[limitx]
    window.set_xticks(ticks,[str(rows[j]["tick"]) for j in x[::2]]+["Limit"])
    window.set_xlabel("Flight ticks (successive doublings)")
    window.set_ylabel("Probability of the window")
    window.set_ylim(-.006,.155)
    window.yaxis.set_major_locator(MaxNLocator(nbins=6))
    window.legend(loc="center right",bbox_to_anchor=(1,.55),frameon=True,
                  framealpha=.94,edgecolor="none",fontsize=8.7)
    fig.savefig(output,dpi=160,facecolor="white",metadata={"Software":"Matplotlib"})
    plt.close(fig)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("result",type=Path)
    parser.add_argument("png",type=Path)
    args=parser.parse_args()
    plot(json.loads(args.result.read_bytes()),args.png)
