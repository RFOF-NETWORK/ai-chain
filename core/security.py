# core/security.py
# de-en: Security primitives for AI-Chain / RFOF-GOLDEN

import hashlib
import os
from typing import List

# Platzhalter – später echte GOLDEN-BIP39-Wortliste
GOLDEN-BIP39_WORDLIST = [
"golden","rfchain","eccu","validator","oracle","ledger","vault","node","anchor","sigma",
"delta","omega","prime","vector","core","seed","block","chain","protocol","sovereign",
"astral","flare","arcane","etheric","radiant","spectral","luminous","aurora","vortex","horizon",
"eclipse","nova","astrion","solstice","ember","halo","prism","ether","astryx","luminar",
"quantum","cipher","matrix","fusion","stellar","gravity","ion","neutron","photon","plasma",
"cosmic","nebula","galaxy","orbit","celestial","radiance","pulse","flux","signal","static",
"dynamic","kinetic","fractal","vectorial","modular","atomic","binary","digital","virtual","synthetic",
"elemental","crystal","obsidian","onyx","marble","granite","basalt","carbon","silicon","titanium",
"cobalt","nickel","mercury","helium","argon","xenon","radon","oxygen","hydrogen","nitrogen",
"circuit","current","voltage","resistor","capacitor","inductor","diode","transistor","quantizer","encoder",
"decoder","compiler","runtime","kernel","system","network","gateway","router","switch","bridge",
"beacon","signal","transmit","receive","broadcast","uplink","downlink","carrier","channel","spectrum",
"frequency","amplitude","phase","vector","scalar","tensor","gradient","integral","derivative","function",
"algorithm","logic","compute","process","thread","parallel","serial","quantize","optimize","synchronize",
"entropy","chaos","order","balance","equilibrium","symmetry","asymmetry","paradox","axiom","theorem",
"proof","lemma","corollary","inference","deduction","induction","abstraction","structure","pattern","sequence",
"origin","genesis","creation","source","root","branch","leaf","stem","core","essence",
"spirit","soul","mind","memory","vision","dream","echo","shadow","light","darkness",
"flare","spark","flash","glow","shine","beam","ray","pulse","wave","ripple",
"storm","tempest","thunder","lightning","wind","breeze","gale","whirl","cyclone","tornado",
"ocean","tide","current","stream","river","lake","pond","spring","waterfall","cascade",
"mountain","summit","peak","ridge","valley","canyon","cliff","plateau","desert","dune",
"forest","grove","meadow","field","prairie","jungle","swamp","marsh","island","archipelago",
"stone","rock","boulder","crystal","gem","diamond","ruby","sapphire","emerald","topaz",
"iron","steel","bronze","silver","gold","platinum","obsidian","quartz","opal","jade",
"ember","coal","ash","smoke","steam","mist","fog","cloud","rain","snow",
"frost","ice","hail","sleet","storm","blizzard","avalanche","quake","eruption","volcano",
"beast","spirit","phantom","wraith","specter","ghost","shade","entity","presence","force",
"guardian","sentinel","watcher","keeper","warden","protector","champion","hero","legend","myth",
"alpha","beta","gamma","delta","epsilon","zeta","eta","theta","iota","kappa",
"lambda","mu","nu","xi","omicron","pi","rho","sigma","tau","upsilon",
"phi","chi","psi","omega","vector","scalar","tensor","matrix","array","index",
"cipher","code","hash","salt","pepper","token","key","lock","vault","safe",
"shield","armor","barrier","wall","gate","portal","door","window","mirror","reflection",
"illusion","mirage","vision","dream","memory","thought","idea","concept","notion","insight",
"wisdom","knowledge","truth","logic","reason","purpose","meaning","value","virtue","honor",
"courage","strength","power","force","energy","motion","momentum","velocity","speed","acceleration",
"gravity","mass","weight","density","volume","space","time","dimension","realm","domain",
"universe","cosmos","multiverse","continuum","infinity","eternity","immortal","infinite","limitless","boundless",
"origin","source","root","seed","sprout","growth","bloom","flower","petal","thorn",
"flame","fire","burn","ignite","kindle","smolder","ember","ash","dust","spark",
"wind","air","sky","cloud","storm","rain","snow","hail","mist","fog",
"earth","soil","stone","rock","metal","ore","crystal","gem","mineral","alloy",
"water","wave","tide","current","flow","stream","river","lake","ocean","sea",
"light","beam","ray","shine","glow","flare","flash","spark","halo","aura",
"shadow","shade","dark","night","void","abyss","rift","chasm","hollow","echo",
"sound","tone","note","chord","melody","rhythm","pulse","beat","vibration","resonance",
"mind","thought","memory","dream","vision","focus","clarity","insight","awareness","consciousness",
"spirit","soul","essence","presence","force","energy","power","will","intent","purpose",
"order","chaos","balance","harmony","discord","entropy","structure","pattern","sequence","cycle",
"alpha","origin","prime","core","root","source","seed","spark","flare","nova",
"astral","stellar","cosmic","galactic","nebular","quantum","etheric","luminous","radiant","spectral",
"arcane","mystic","ancient","eternal","infinite","timeless","boundless","limitless","sovereign","supreme",
"ascend","rise","elevate","transcend","unite","merge","fuse","bind","forge","shape",
"craft","form","build","create","design","invent","discover","explore","journey","venture",
"signal","transmit","receive","broadcast","encode","decode","encrypt","decrypt","compute","process",
"kernel","system","network","cluster","node","server","client","gateway","router","switch",
"vector","tensor","matrix","array","logic","reason","method","function","algorithm","protocol",
"anchor","vault","ledger","oracle","chain","block","token","coin","credit","asset",
"trust","proof","verify","validate","confirm","attest","sign","seal","stamp","record",
"memory","cache","buffer","stack","queue","stream","flow","pulse","cycle","loop",
"origin","root","source","cause","effect","result","outcome","impact","force","motion",
"vision","dream","idea","concept","insight","wisdom","truth","logic","reason","purpose",
"flare","spark","ember","glow","shine","beam","flash","halo","aura","radiance",

"BIP39"]


def double_sha256(data: str) -> str:
    """
    Double SHA-256 hashing for passwords, phrases, ids.
    """
    b = data.encode("utf-8")
    return hashlib.sha256(hashlib.sha256(b).digest()).hexdigest()


def generate_entropy(bits: int = 256) -> bytes:
    return os.urandom(bits // 8)


def entropy_to_mnemonic(entropy: bytes, words_count: int = 24) -> List[str]:
    """
    Placeholder BIP39-like mnemonic generator.
    In production: replace with real BIP39 implementation.
    """
    digest = hashlib.sha256(entropy).digest()
    words: List[str] = []
    i = 0
    while len(words) < words_count:
        b = digest[i % len(digest)]
        idx = b % len(BIP39_WORDLIST)
        words.append(BIP39_WORDLIST[idx])
        i += 1
    return words


def generate_mnemonic_24() -> List[str]:
    entropy = generate_entropy(256)
    return entropy_to_mnemonic(entropy, 24)


def derive_address_from_mnemonic(mnemonic: List[str]) -> str:
    """
    Simple deterministic address derivation from mnemonic.
    RFOF-GOLDEN style: AIC + first 40 hex chars of double_sha256.
    """
    joined = " ".join(mnemonic)
    h = double_sha256(joined)
    return "AIC" + h[:40]

