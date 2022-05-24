import math
from shell.env import ENV

from system.filesystem import File, Node
from system.usrbin_programs import usrbin_progs

from gui.plotter import MeshPlotter
from puzzle.dday_puzzle.programs.histogram import Histogram
from puzzle.dday_puzzle.programs.sub_password import UnlockSubPassword

from .ciphers.ciphers import build_cipher_graph
from .wordplay.wordplay import build_emoji_graph
from .tutorial.tutorial import build_tutorial_graph
from .fanfic.fanfic import build_fanfic_graph
from .physical.physical import build_physical_graph


CIPHER_DIR = "puzzle/dday_puzzle/ciphers"
CIPHER_TEXT =\
"""
Cipher: Columnar Transposition
ORCHN    AERTA    EEECU
BHEMS    AAAOT    MTTMY
MTTMY    TFVEO    EFLOT
MOACI    LUAAN    RRCHN
EFLOT    LNDGY    MOACI
NEECU    HKINI    HBHEM
"""
SUB_CIPHER = File("vault-lock-2-cipher.txt",
"""
dcwy nve tx ne zvyd xldbe iub v fcwzx. vy iub fce, w fwzz pxxs wd tbwxi: wd vssxvby dcvd dcx fubyd cvy cvssxlxm; dcx
wlydwdkdwul cvy mwyjuhxbxm ukb bxyxvbjc ul dcx hvbwvld. w mu lud pluf xgvjdze cuf nkjc dcxe pluf vtukd wd, lub wi dcxe
pluf dcvd w fvy dcx ulx fcu cvy txxl mxysxbvdxze dbewlr du juhxb wd ks.

w pluf dcxe fvld dcx hvbwvld. w pluf dcvd dcxe fwzz mu vledcwlr du rxd dcxwb cvlmy ul wd. zwx, ydxvz, xhxl mwysuyx…
ludcwlr wy duu xgdbxnx iub dcx wlydwdkdwul.

dcxe pluf dcvd dcx hvbwvld jvl ywlrzx-cvlmxmze vzzuf dcxn du dvpx uhxb dcx fubzm. yu iub luf, w fwzz nvpx neyxzi yjvbjx.
w fwzz dbe du cwmx vy nkjc ui dcx bxnvwlwlr bxyxvbjc vy w jvl, wljzkmwlr dcx hvbwvld wdyxzi. w cusx dcvd w jvl ykjjxxm.
w cusx dcvd fcuxhxb iwlmy ne fubp... wi vle... dcvd dcxe fwzz pluf dcx bwrcd dcwlr du mu.
"""
)


# TODO: Hint files
def build_final_nodes(word, phys, fan):
    def unhide(n: Node):
        def _func(_):
            n.hidden = False
        return _func

    # Trans
    trans_cont = Node("Integrity", parents=[phys], hidden=True)
    trans = Node("vault-lock-1", parents=[trans_cont])
    trans.prompt = CIPHER_TEXT
    trans.set_password("Honor")
    trans_cont.directory.add_file(File("transposition.pdf", filepath=(CIPHER_DIR+"/transposition/transposition.pdf")))
    trans_cont.add_entry_callback(unhide(trans_cont))

    # Sub
    sub_cont = Node("Tenacity", parents=[word], hidden=True)
    sub = Node("vault-lock-2", parents=[sub_cont])
    sub_cont.directory.add_file(SUB_CIPHER)
    sub.set_password("jrhtywxvfcundmzkqgpboaiesl")
    sub_cont.directory.add_file(File("hint.txt", "We have provided you with a 'count' program to look at character distributions."))

    hist_prog = Histogram()
    sub_unlock = UnlockSubPassword(hidden=True)
    sub_cont.directory.add_program(sub_unlock.NAME, sub_unlock)
    sub_cont.add_entry_callback(lambda _: ENV.visible_progs.add(Histogram))
    ENV.path[hist_prog.NAME] = hist_prog

    sub_cont.directory.add_file(File("frequency.pdf", filepath=(CIPHER_DIR+"/substitution/frequency.pdf")))
    sub_cont.directory.add_file(File("substitution.pdf", filepath=(CIPHER_DIR+"/substitution/substitution.pdf")))

    sub_cont.add_entry_callback(unhide(sub_cont))

    # Men
    men_cont = Node("Creativity", parents=[fan], hidden=True)
    men = Node("vault-lock-3", parents=[men_cont])
    men.prompt = "{Who} cant do {what}? (You'll have to read the whole story, or ask the alumn)."
    men.set_password("men pregnant")

    men_cont.add_entry_callback(unhide(men_cont))

    # Vault
    lock = Node("Vault-Lock", parents=[trans, sub, men])
    lock.set_lock_func(lambda _: trans.locked() or sub.locked() or men.locked())
    lock.directory.add_file(File("Success.txt", "Congratulations! You made it through and cracked the vault! Talk to your alumn for more information."))

    c1 = 0.5
    c2 = math.sqrt(3) / 4
    pts = [(-c1, -c2), (0, c2), (c1, -c2), (0,0)]
    ids = [sub_cont.id, men_cont.id, trans_cont.id, lock.id]
    return MeshPlotter(pts, ids)


def build_graph():
    # Setup ENV
    ENV.reset()
    ENV.path = usrbin_progs()

    # Build graph
    start_msg = "AveryOs (TODO)"
    tutorial_nodes, tutorial_mesh, start_msg = build_tutorial_graph()
    word_nodes, word_mesh = build_emoji_graph()
    fanfic_nodes, fanfic_mesh = build_fanfic_graph()
    physical_nodes, physical_mesh = build_physical_graph()

    final_mesh = build_final_nodes(word_nodes[-1], physical_nodes[-1], fanfic_nodes[-1])

    root = tutorial_nodes[0]
    start = tutorial_nodes[-1]

    start.add_child(word_nodes[0])
    start.add_child(fanfic_nodes[0])
    start.add_child(physical_nodes[0])

    # Combine meshes
    mesh = MeshPlotter([],[],radius=75)

    # TODO: fanfic mesh
    tutorial_mesh = tutorial_mesh.transform(scale=50, shift=(0,1500), angle=180)
    word_mesh = word_mesh.transform(scale=50, shift=(-400,0), angle=-90)
    physical_mesh = physical_mesh.transform(scale=50, shift=(400,0), angle=90)
    fanfic_mesh = fanfic_mesh.transform(scale=50, shift=(0,-300), angle=90)
    final_mesh = final_mesh.transform(scale=500, shift = (-1000,-1500), angle=180)

    mesh.extend(tutorial_mesh)
    mesh.extend(word_mesh)
    mesh.extend(physical_mesh)
    mesh.extend(fanfic_mesh)
    mesh.extend(final_mesh)

    ENV.plotter = mesh
    
    return root, start_msg
