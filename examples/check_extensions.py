"""Exact quartic distribution identities and the same-polar six/eight-flex examples."""
from pathlib import Path
import hashlib, json, os, time
import sympy as s
def io(p):
    t=os.path.abspath(p)
    return Path(t if os.name!="nt" or t.startswith("\\\\?\\") else "\\\\?\\"+t)
x,y,z,b=s.symbols("x y z b")
P=y*(x-y)*(x-2*y)*(x-3*y)
p=s.expand(P.subs(x,1))
V=z**4/s.Integer(12)+(y*y-1)*z*z/2+b
d=s.diff(p,y).subs(y,1)
h1=-V.subs(y,1)/d
h2=s.expand(-(s.diff(p,y,2).subs(y,1)*h1*h1/2+s.diff(V,y).subs(y,1)*h1)/d)
checks={
 "first_graph_coefficient":s.expand(h1-b/2-z**4/24)==0,
 "normalized_flex_leading":s.diff(h1,z,2)==z*z/2,
 "double_root_unfolding_coefficient":s.simplify(s.diff(h2,z,2).subs(z,0)-b/2)==0,
 "kernel_same_second_polar":s.diff(b*x**4,z,2)==0,
 "quartic_discriminant_identity":True,
}
a,l,q,t=s.symbols("a l q t")
checks["quartic_discriminant_identity"]=s.discriminant(a*t*t+l*t+q,t)==l*l-4*a*q
cases=[]
for bv,want in [(1,6),(-1,8)]:
    started=time.perf_counter()
    F=12000*P+z**4+6*(y*y-x*x)*z*z+12*bv*x**4
    H=s.Poly(s.hessian(F,(x,y,z)).det(),x,y,z).primitive()[1].as_expr()
    f,h=F.subs(z,1),H.subs(z,1)
    seq=s.subresultants(f,h,y)
    E=s.Poly(seq[-1],x).primitive()[1]
    linear=s.Poly(seq[-2],y)
    A=s.Poly(linear.coeff_monomial(y),x)
    inf=s.Poly(F.subs({x:1,z:0}),y)
    hinf=s.Poly(H.subs({x:1,z:0}),y)
    conditions={
     "quartic_leading_coefficient":s.Poly(f,y).LC()==-72000,
     "eliminant_degree_24":E.degree()==24,
     "eliminant_squarefree":s.gcd(E,E.diff()).degree()==0,
     "linear_subresultant":linear.degree()==1,
     "linear_denominator_coprime":s.gcd(E,A).degree()==0,
     "affine_complex_smoothness":list(s.groebner([f,s.diff(f,x),s.diff(f,y)],x,y))==[1],
     "no_curve_point_x0_at_infinity":F.subs({x:0,y:1,z:0})!=0,
     "infinity_complex_smoothness":s.gcd(inf,inf.diff()).degree()==0,
     "no_flex_at_infinity":s.gcd(inf,hinf).degree()==0,
     "expected_real_count":int(E.count_roots(-s.oo,s.oo))==want
    }
    cases.append(dict(b=bv,mu="1/1000",expected=want,real_affine_count=int(E.count_roots(-s.oo,s.oo)),
      checks=conditions,passed=sum(conditions.values()),total=len(conditions),
      eliminant=str(E.as_expr()),elapsed_seconds=time.perf_counter()-started))
out=dict(scope="Exact identities and two quartics at a fixed parameter; not a proof for arbitrary degree or parameter",
 symbolic_checks=checks, h1=str(h1),h2=str(h2),cases=cases,
 sympy=s.__version__,script_sha256=hashlib.sha256(io(__file__).read_bytes()).hexdigest())
io(Path(__file__).with_name("EXTENSION_CHECKS.json")).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
if not all(checks.values()) or any(r["passed"]!=r["total"] for r in cases):
    raise RuntimeError("Extension checks failed")
print(json.dumps({"symbolic":sum(checks.values()),"cases":[{k:r[k] for k in ("b","passed","total","real_affine_count","elapsed_seconds")} for r in cases]}))
