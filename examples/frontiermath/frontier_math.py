from inspect_ai import Task, task
from inspect_ai.dataset import Sample

# Attempt to import solver & scorer from the current package first (installed mode)
try:
    from .agent import frontiermath_agent
    from .scorer import verification_code_scorer
except ImportError:  # Fallback when running the file directly
    from agent import frontiermath_agent
    from scorer import verification_code_scorer

# -----------------------------------------------------------------------------
#  Problem definitions
# -----------------------------------------------------------------------------
# Each problem is defined by a plain-English question and its verified answer.
# -----------------------------------------------------------------------------
PROBLEMS: list[tuple[str, int]] = [
    (
        "For a positive integer $n$, let $v_p(n)$ denote the largest integer $v$ such that $p^v \mid n$. For a prime $p$ and $a \\not\\equiv 0 \\pmod{p}$, let $\\text{ord}_p(a)$ denote the smallest positive integer $o$ such that $a^o \\equiv 1 \\pmod{p}$. For $x > 0$, let\\n$$\\text{ord}_{p, x}(a) = \\prod_{\\substack{q \\le x \\ q \\text{ prime}}} q^{v_q(\\text{ord}_p(a))} \\prod_{\\substack{q > x \\ q \\text{ prime}}} q^{v_q(p-1)}.$$$$\\nLet $S_x$ denote the set of primes $p$ for which\\n$$\\text{ord}_{p, x}(2) > \\text{ord}_{p, x}(3),$$\\nand let $d_x$ denote the density\\n$$d_x = \\frac{|S_x|}{|\\{p \\le x : p \\text{ is prime}\\}|}$$\\nof $S_x$ in the primes. Let\\n$$d_{\\infty} = \\lim_{x \\to \\infty} d_x.$$$$\\nCompute $\\lfloor 10^6 d_{\\infty} \\rfloor.$",
        367_707,
    ),
    (
        "Let $a_n$ for $n \\in \\mathbb{Z} $ be the sequence of integers satisfying the recurrence formula\\n$$a_n = 198130309625 a_{n-1} + 354973292077 a_{n-2} - 427761277677 a_{n-3} + 370639957 a_{n-4}$$\\nwith initial conditions $a_i=i$ for $0 \\leq i \\leq 3$. Find the smallest prime $ p \\equiv 4 \\pmod{7}$ for which the function\\n$\\mathbb{Z} \\rightarrow \\mathbb{Z}$ given by $ n \\mapsto a_n$ can be extended to a continuous function on $\\mathbb{Z}_p$.",
        9_811,
    ),
    (
        "Construct a degree 19 polynomial $p(x) \\in \\mathbb{C}[x]$ such that $X:=\\{p(x) = p(y)\\} \\subset \\mathbb{P}^1 \\times \\mathbb{P}^1$ has at least 3 (but not all linear) irreducible components over $\\mathbb{C}$. Choose $p(x)$ to be odd, monic, have real coefficients and linear coefficient -19 and calculate $p(19)$.",
        1_876_572_071_974_094_803_391_179,
    ),
    (
        "Let $M_{1000}^4$ be the set of $4$-tuples of invertible $1000 \\times 1000$ matrices with coefficients in $\\mathbb{C}$. Let $S\\subset M_{1000}^4$ be the subset of all tuples $(A_1,A_2,A_3,A_4)$ satisfying the conditions:\\n\\begin{align}\\nA_i^2 &= I, &&\\quad \\text{for all } 1\\le i\\le 4\\\\\\nA_iA_j &= A_jA_i, &&\\quad \\text{if } \\{3j- i, 3i-j\\} \\cap 5\\mathbb{Z}_{>0} =\\emptyset \\\\\
A_iA_jA_i^{-1}A_j^{-1} &= A_jA_i, &&\\quad \\text{if } \\{3j- i, 3i-j\\} \\cap 5\\mathbb{Z}_{>0} \\neq\\emptyset,\\n\\end{align}\\nwhere $5\\mathbb{Z}_{>0}$ refers to the set of positive multiples of $5$, i.e., $5\\mathbb{Z}_{>0} = \\{5,10,15,\\dots\\}$.\\nThe group $G = GL(1000)$ of invertible complex $1000 \\times 1000$ matrices acts on $S$ by the formula:\\n$$B \\cdot (A_1,A_2,A_3,A_4) = (BA_1B^{-1}, BA_2B^{-1}, BA_3B^{-1}, BA_4B^{-1}).$$\\nFind the number of orbits of this action, i.e., find $|S/G|$.",
        625_243_878_951,
    ),
    (
        "How many nonzero points are there on $$x^3y+y^3z+z^3x=0$$ over $\\mathbb{F}_{5^{18}}$ up to scaling?",
        3_814_708_984_376,
    ),
    (
        "Let $U\\subset\\mathbb{P}H^0(\\mathbb{P}^2_{\\mathbb{Z}}, \\mathcal{O}(2))$ be the space of smooth conics in $\\mathbb{P}^2_{\\mathbb{Z}}$, and let\\n$Z\\subset U^6$ be the closed subscheme parametrizing $6$-tuples $(C_1, \\cdots, C_6)$ with $C_1$ tangent to $C_2, \\cdots, C_6$. Let $\\pi: Z\\to C^5$\\nbe the map induced by the projection onto the last $5$ coordinates, and let $V\\subset U^5$ be the dense open subscheme over which $\\pi$ is finite \\'etale.\\nLet $$L=\\lim_{p\\to \\infty} \\frac{1}{\\#V(\\mathbb{F}_p)}\\sum_{x\\in V(\\mathbb{F}_p)} \\#\\pi^{-1}(x),$$\\nthat is, the limit of the average number of components of the space of conics tangent to 5 smooth conics over $\\mathbb{F}_p$, as $p$ tends to infinity (when this space is finite \\'etale).\\n\\nFind $\\lfloor 100L \\rfloor.$",
        866,
    ),
    (
        "There are unique constants $C, \\alpha, \\beta$ such that the number of solutions to the equation\\n\\n$$ab+1=cde$$\\n\\nwith $a, b, c, d, e \\in \\mathbb{N}$ with $ab \\le x$ is asymptotic to $Cx^{\\alpha}\\log^{\\beta}x$ as $x\\rightarrow\\infty.$\\n\\nCompute $\\lfloor 1000C\\rfloor.$",
        214,
    ),
    (
        "\\textit{Background.} \\nThe \\emph{Tsirelson space} is a Banach space introduced in 1974 as a counterexample to a longstanding conjecture in Banach space theory. It is a subspace of $\\ell^{\\infty}$ described as follows. \\n\\nLet $P_k$ denote the operator on $\\ell^{\\infty}$ that modifies each $\\langle x_n:\, n \\in \\mathbb N \\rangle \\in \\ell^{\\infty}$ by setting the first $k$ coordinates equal to $0$ (without changing any other coordinates). Given $\\vec x = \\langle x_n:\, n \\in \\mathbb N \\rangle \\in \\ell^{\\infty}$, the \\emph{support} of $\\vec x$ is $\\mathrm{supp}(\\vec x) = \\{ n \\in \\mathbb N :\\, x_n \\neq 0 \\}$. \\nThe Tsirelson space is the span of the smallest pointwise-closed subset $K$ of the unit ball in $\\ell^{\\infty}$ satisfying the following two properties:\\n\\n1. For every $j \\in \\mathbb N$, the unit vector $\\vec e_j$ and all its multiples $\\lambda \\vec e_j$ with $|\\lambda| \\leq 1$ belong to $K$.\\n\\n2. Suppose $\\vec x_1,\\dots,\\vec x_k$ is a finite sequence of members of $K$, each with finite support, such that $\\max (\\mathrm{supp}(\\vec x_i)) < \\min (\\mathrm{supp}(\\vec x_j))$ for all $i < j \\leq k$. Then $\\frac{1}{2}P_k(\\vec x_1 + \\dots + \\vec x_k) \\in K$.\\n\\n\\textit{Problem.}\\n\\nLet $N$ denote the largest natural number such that \\nthere is a member $\\langle x_n:\, n \\in \\mathbb N \\rangle$ of the set $K$ described above with \\n$x_3 = 1/2$, $x_N > 1/20$, and \\n$x_i > x_j$ whenever $3 \\leq i < j \\leq N$. \\nIt turns out that $N$ is too large to write down in a reasonable amount of space, so let us ask instead: what is the largest power of $2$ dividing $N$? In other words, find the integer $p \\geq 0$ such that $N = m2^p$ for some odd number $m$.",
        402_653_211,
    ),
    (
        "Let $W$ be the set of finite words with all distinct letters over the alphabet of positive integers. Define a function $F:W\\rightarrow W$ recursively as follows. First, let $F(\\epsilon)=\\epsilon$, where $\\epsilon$ is the empty word. Given a nonempty word $w\\in W$, let $F(w)=F(L)F(R)m$, where $m$ is the largest number in $w$ and $w=LmR$. Let $n=10^{12}$, and note that $W$ restricts to a function from $S_n$ to itself, where $S_n$ is the symmetric group of order $n$. Let $\\sigma$ be a permutation chosen uniformly at random from $S_n$, and let $X$ be the expected number of integers $1\\le i<n$ such that $F(\\sigma)(i+1)<F(\\sigma)(i)$. Compute $\\lfloor X\\rfloor$.",
        499_999_999_972,
    ),
    (
        "Let $\\mathcal P$ be a regular $101$-gon of circumradius $1$. Draw each diagonal of $\\mathcal P$ with probability 0.001. This splits $\\mathcal P$ into several closed regions. Let $E$ be the expected value of the perimeter of the region containing the center of $\\mathcal P$.\\n\\nCompute $\\lfloor 10^9 E \\rfloor.$",
        4_771_880_153,
    ),
]


def _make_sample(question: str, answer: int) -> Sample:
    """Factory that wraps a question/answer pair in a :class:`~inspect_ai.dataset.Sample`."""
    return Sample(
        input=question,
        metadata={
            "answer_type": "Python int",
            "verification_code": f"def verify(a):\n    return a == {answer}",
        },
    )


@task
def frontier_math() -> Task:
    """Frontier mathematics challenge with advanced problems."""

    return Task(
        dataset=[_make_sample(q, a) for q, a in PROBLEMS],
        solver=[frontiermath_agent()],
        scorer=verification_code_scorer(),
    )
