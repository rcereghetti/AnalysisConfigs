from collections.abc import Iterable
import awkward as ak


def lepton_veto(events, params, **kwargs):
    no_electron = events.nElectronGood == 0
    no_muon = events.nMuonGood == 0

    mask = no_electron & no_muon

    return ak.where(ak.is_none(mask), False, mask)


def four_jet(events, params, **kwargs):
    no_electron = events.nElectronGood == 0
    no_muon = events.nMuonGood == 0

    mask_4jet = events.nJetGood >= params["njet"]
    mask = mask_4jet & no_electron & no_muon

    return ak.where(ak.is_none(mask), False, mask)


def jet_pt(events, params, **kwargs):
    no_electron = events.nElectronGood == 0
    no_muon = events.nMuonGood == 0
    mask_4jet = events.nJetGood >= params["njet"]
    mask_4jet_nolep = mask_4jet & no_electron & no_muon

    mask_4jet_nolep_none = ak.mask(mask_4jet_nolep, mask_4jet_nolep)
    jets_btag_order = events[mask_4jet_nolep_none].JetGoodHiggs

    jets_pt_order = jets_btag_order[
        ak.argsort(jets_btag_order.pt, axis=1, ascending=False)
    ]

    mask = (
        (jets_pt_order.pt[:, 0] > params["pt_jet0"])
        & (jets_pt_order.pt[:, 1] > params["pt_jet1"])
        & (jets_pt_order.pt[:, 2] > params["pt_jet2"])
        & (jets_pt_order.pt[:, 3] > params["pt_jet3"])
    )
    return ak.where(ak.is_none(mask), False, mask)


def jet_btag_lead(events, params, **kwargs):
    no_electron = events.nElectronGood == 0
    no_muon = events.nMuonGood == 0
    mask_4jet = events.nJetGood >= params["njet"]
    mask_4jet_nolep = mask_4jet & no_electron & no_muon

    mask_4jet_nolep_none = ak.mask(mask_4jet_nolep, mask_4jet_nolep)
    jets_btag_order = events[mask_4jet_nolep_none].JetGoodHiggs

    jets_pt_order = jets_btag_order[
        ak.argsort(jets_btag_order.pt, axis=1, ascending=False)
    ]

    mask_pt = (
        (jets_pt_order.pt[:, 0] > params["pt_jet0"])
        & (jets_pt_order.pt[:, 1] > params["pt_jet1"])
        & (jets_pt_order.pt[:, 2] > params["pt_jet2"])
        & (jets_pt_order.pt[:, 3] > params["pt_jet3"])
    )

    mask_btag = (
        jets_btag_order.btagPNetB[:, 0] + jets_btag_order.btagPNetB[:, 1]
    ) / 2 > params["mean_pnet_jet"]

    mask = mask_pt & mask_btag

    return ak.where(ak.is_none(mask), False, mask)


def jet_btag_all(events, params, **kwargs):
    no_electron = events.nElectronGood == 0
    no_muon = events.nMuonGood == 0
    mask_4jet = events.nJetGood >= params["njet"]
    mask_4jet_nolep = mask_4jet & no_electron & no_muon

    mask_4jet_nolep_none = ak.mask(mask_4jet_nolep, mask_4jet_nolep)
    jets_btag_order = events[mask_4jet_nolep_none].JetGoodHiggs

    jets_pt_order = jets_btag_order[
        ak.argsort(jets_btag_order.pt, axis=1, ascending=False)
    ]

    mask_pt = (
        (jets_pt_order.pt[:, 0] > params["pt_jet0"])
        & (jets_pt_order.pt[:, 1] > params["pt_jet1"])
        & (jets_pt_order.pt[:, 2] > params["pt_jet2"])
        & (jets_pt_order.pt[:, 3] > params["pt_jet3"])
    )

    mask_btag = (
        (
            (jets_btag_order.btagPNetB[:, 0] + jets_btag_order.btagPNetB[:, 1]) / 2
            > params["mean_pnet_jet"]
        )
        & (jets_btag_order.btagPNetB[:, 2] > params["third_pnet_jet"])
        & (jets_btag_order.btagPNetB[:, 3] > params["fourth_pnet_jet"])
    )

    mask = mask_pt & mask_btag

    return ak.where(ak.is_none(mask), False, mask)


def hh4b_presel_cuts(events, params, **kwargs):
    at_least_four_jets = events.nJetGood >= params["njet"]
    no_electron = events.nElectronGood == 0
    no_muon = events.nMuonGood == 0

    mask_4jet_nolep = at_least_four_jets & no_electron & no_muon

    # convert false to None
    mask_4jet_nolep_none = ak.mask(mask_4jet_nolep, mask_4jet_nolep)
    jets_btag_order = events[mask_4jet_nolep_none].JetGood  # HERE_OLD_CUTS JetGoodHiggs

    jets_pt_order = jets_btag_order[
        ak.argsort(jets_btag_order.pt, axis=1, ascending=False)
    ]

    mask_pt_none = (
        (jets_pt_order.pt[:, 0] > params["pt_jet0"])
        & (jets_pt_order.pt[:, 1] > params["pt_jet1"])
        & (jets_pt_order.pt[:, 2] > params["pt_jet2"])
        & (jets_pt_order.pt[:, 3] > params["pt_jet3"])
    )
    # convert none to false
    mask_pt = ak.where(ak.is_none(mask_pt_none), False, mask_pt_none)

    mask_btag = (
        (jets_btag_order.btagPNetB[:, 0] + jets_btag_order.btagPNetB[:, 1]) / 2
        > params["mean_pnet_jet"]
    )

    mask_btag = ak.where(ak.is_none(mask_btag), False, mask_btag)

    mask = mask_pt & mask_btag

    # Pad None values with False
    return ak.where(ak.is_none(mask), False, mask)

def hh4b_2b_cuts(events, params, **kwargs):
    jets_btag_order = events.JetGoodHiggs

    mask = (jets_btag_order.btagPNetB[:, 2] < params["third_pnet_jet"]) & (
        jets_btag_order.btagPNetB[:, 3] < params["fourth_pnet_jet"]
    )

    # Pad None values with False
    return ak.where(ak.is_none(mask), False, mask)

def hh4b_4b_cuts(events, params, **kwargs):
    jets_btag_order = events.JetGoodHiggs

    mask = (jets_btag_order.btagPNetB[:, 2] > params["third_pnet_jet"]) & (
        jets_btag_order.btagPNetB[:, 3] > params["fourth_pnet_jet"]
    )

    # Pad None values with False
    return ak.where(ak.is_none(mask), False, mask)

def VBF_cuts(events, params, **args):
    at_least_two_vbf = events.nJetGoodVBF >= params["njet_vbf"]
    mask_delta_eta = events.deltaEta > params["delta_eta"]

    mask = at_least_two_vbf = mask_delta_eta

    return mask 

def VBF_generalSelection_cuts(events, params, **kwargs):
    at_least_two_jets = events.nJetVBF_generalSelection >= params["njet_vbf"]
    mask_two_vbf_jets = ak.mask(at_least_two_jets, at_least_two_jets)
    jets_btag_order = events[mask_two_vbf_jets].JetVBF_generalSelection

    jets_pt_order = jets_btag_order[
        ak.argsort(jets_btag_order.pt, axis=1, ascending=False)
    ]

    mask_VBF_pt_none = (
        (jets_pt_order.pt[:, 0] > params["pt_VBFjet0"])
    )

    # convert none to false
    mask_pt = ak.where(ak.is_none(mask_VBF_pt_none), False, mask_VBF_pt_none)

    #No jets on the same side
    mask_no_same_side = (events[mask_two_vbf_jets].JetVBF_generalSelection.eta[:, 0] *
                          events[mask_two_vbf_jets].JetVBF_generalSelection.eta[:, 1] < 
                          params["eta_product"])

    mask_mass = (events.jj_mass > params["mjj"])

    mask = mask_pt & mask_no_same_side & mask_mass

    return mask

def qvg_cuts(events, params, **kwargs):
    JetGoodVBF_padded = ak.pad_none(events.JetGoodVBF, 2) #Adds none jets to events that have less than 2 jets
    mask = ak.Array((JetGoodVBF_padded.btagPNetQvG[:, 0] > params["qvg_cut"]) &
           (JetGoodVBF_padded.btagPNetQvG[:, 1] > params["qvg_cut"]))

    return mask