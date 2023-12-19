from pocket_coffea.lib.cut_definition import Cut
import awkward as ak

def ptbin(events, params, **kwargs):
    # Mask to select events in a GenJet pt bin
    if params["pt_high"] == "Inf":
        mask = events.GenJet.pt > params["pt_low"]
    elif type(params["pt_high"]) != str:
        mask = (events.GenJet.pt > params["pt_low"]) & (
            events.GenJet.pt < params["pt_high"]
        )
    else:
        raise NotImplementedError

    # mask = ak.where(ak.is_none(mask, axis=1), False, mask)
    # mask=mask[~ak.is_none(mask, axis=1)]

    assert not ak.any(ak.is_none(mask, axis=1)), f"None in ptbin"#\n{events.nJetGood[ak.is_none(mask, axis=1)]}"

    return mask


def get_ptbin(pt_low, pt_high, name=None):
    if name == None:
        name = f"pt{pt_low}to{pt_high}"
    return Cut(
        name=name,
        params={"pt_low": pt_low, "pt_high": pt_high},
        function=ptbin,
        collection="GenJet",
    )


# do th same for eta
def etabin(events, params, **kwargs):
    # Mask to select events in a GenJet eta bin
    mask = (events.Jet.eta > params["eta_low"]) & (
        events.Jet.eta < params["eta_high"]
    )
    # substitute none with false in mask
    # mask = ak.where(ak.is_none(mask, axis=1), False, mask)
    # mask=mask[~ak.is_none(mask, axis=1)]



    assert not ak.any(ak.is_none(mask, axis=1)), f"None in etabin"#\n{events.nJetGood[ak.is_none(mask, axis=1)]}"

    return mask


def get_etabin(eta_low, eta_high, name=None):
    if name == None:
        name = f"eta{eta_low}to{eta_high}"
    return Cut(
        name=name,
        params={"eta_low": eta_low, "eta_high": eta_high},
        function=etabin,
        collection="Jet",
    )
