"""One exact nonradial quartic at mu=1/1000, via elimination and Sturm.

No floating-point roots are used. A linear subresultant and coprimality
justify reading real affine intersection points from the eliminant.
"""
from pathlib import Path
import hashlib
import json
import time
import sympy as s

started=time.perf_counter()
x,y,z=s.symbols('x y z')
P=y*(x-y)*(x-2*y)*(x-3*y)
F=12000*P+z**4-6*x*x*z*z+12*y*y*z*z
H=s.Poly(s.hessian(F,(x,y,z)).det(),x,y,z).primitive()[1].as_expr()
f=F.subs(z,1)
h=H.subs(z,1)
chain=s.subresultants(f,h,y)
R=s.Poly(chain[-1],x).primitive()[1]
linear=s.Poly(chain[-2],y)
a=s.Poly(linear.coeff_monomial(y),x)
b=s.Poly(linear.coeff_monomial(1),x)
checks={
    'leading_coefficient_of_f_in_y_nonzero_constant': s.Poly(f,y).LC()==-72000,
    'penultimate_subresultant_is_linear': linear.degree()==1,
    'eliminant_squarefree': s.gcd(R,R.diff()).degree()==0,
    'linear_denominator_coprime_to_eliminant': s.gcd(R,a).degree()==0,
}
real_count=int(R.count_roots(-s.oo,s.oo))
checks['six_real_affine_flexes']=real_count==6
Hinf=s.factor(H.subs(z,0))
infinity_points=[(1,0,0)]+[(j,1,0) for j in (1,2,3)]
checks['no_inflections_at_infinity']=all(Hinf.subs({x:p[0],y:p[1]})!=0 for p in infinity_points)
# Prove smoothness on the real and complex projective curve at this parameter.
affine_singular=s.groebner([f,s.diff(f,x),s.diff(f,y)],x,y)
checks['affine_complex_smoothness']=list(affine_singular)==[1]
checks['infinity_smoothness']=all(any(s.diff(F,v).subs(dict(zip((x,y,z),p)))!=0
                                         for v in (x,y,z)) for p in infinity_points)
checks['intersection_degree_is_24']=R.degree()==24
out=dict(scope='One exact quartic, mu=1/1000; distinct ordinary projective real flexes',
         F=str(s.expand(F)),mu='1/1000',eliminant=str(R.as_expr()),
         eliminant_degree=R.degree(),real_affine_count=real_count,real_infinity_count=0,
         linear_subresultant_degree=linear.degree(),checks=checks,
         passed=sum(checks.values()),total=len(checks),elapsed_seconds=time.perf_counter()-started,
         sympy=s.__version__,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         explanation='Squarefree eliminant and coprime linear subresultant give 24 simple complex affine intersections and six real ones. There are no infinity flexes. Smoothness is checked separately.',
         general_degree_statement=False)
Path(__file__).with_name('QUARTIC_CHECK.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ('passed','total','real_affine_count','eliminant_degree','elapsed_seconds')}))
if not all(checks.values()):
    print(checks)
    raise SystemExit(1)
