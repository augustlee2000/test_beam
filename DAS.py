import datetime
then = datetime.datetime.now()
print ("Start date and time: ", then.strftime("%Y-%m-%d %H:%M:%S"))

#!/usr/bin/env python
from exampleModule import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True



def MakeHist(N,colors,names,title,x_axis,y_axis,high,low,bins):
    hist = []
    for i in range(N):
        hists = ROOT.TH1F(names[i],title,bins,low,high)
        hists.SetLineColor(colors[i])
        #hists.SetFillColor(colors[i])
        hists.GetXaxis().SetTitle(x_axis)
        hists.GetYaxis().SetTitle(y_axis)
        hist.append(hists)
    return hist


def CMSLabel(x,y,color,name):
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextColor(ROOT.kBlack)
    l.DrawLatex(x,y,"CMS")


    delx = (0.115*496*ROOT.gPad.GetWh())/(472*ROOT.gPad.GetWw()) #696

    t =ROOT.TLatex()
    t.SetNDC()
    t.SetTextFont(42)
    t.SetTextColor(ROOT.kBlack)
    t.DrawLatex(x+delx,y,name)



def HistNorm(hist):
    integral = hist.Integral()
    hist.Scale(1./integral)


def Label(x,y,name):
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.SetTextColor(ROOT.kBlack)
    l.DrawLatex(x,y,name)

def legends(hists):
    print("name = ",hists.GetName())
    hists_legend.AddEntry(hists,hists.GetName(),"lp")


from array import array

file1 = ROOT.TFile("/eos/uscms/store/user/cmsdas/2023/short_exercises/Tau/TTTo2L2Nu__1656732C-0CD4-F54B-B39D-19CA08E18A77.root","READ")
tree = file1.Get("Events")


colors=[ROOT.kBlue,ROOT.kRed, ROOT.kBlack, ROOT.kGreen]
names = ["Di Tau Mass " ]
names2 =["Number of BJets in Event" ]

hist_array = MakeHist(1,colors,names,"TTBar:  DiTau Mass" ,"Mass (GeV)","Normalized Instances",100,40,75)
hist_array2 = MakeHist(1,colors,names2,"TTBar: Btagged Jets Number" ,"Mass (GeV)","Normalized Instances",5,0,5)



#tree.Print()
total_btagged = 0
total_jet = 0
for ientry in range(tree.GetEntries()): #tree.GetEtnries()
        bjets_in_event = 0
        tree.GetEntry(ientry)
        if tree.nTau>1:
                fourVecArray = np.array([])
                for i in range(len(tree.Tau_eta)):
                        DeepTauJet = tree.Tau_idDeepTau2017v2p1VSjet[i]

                        if DeepTauJet >="\x08" :
                                vec_1 = ROOT.TLorentzVector()
                                vec_1.SetPtEtaPhiM(tree.Tau_pt[i], tree.Tau_eta[i], tree.Tau_phi[i], tree.Tau_mass[i])
                                fourVecArray = np.append(fourVecArray, vec_1)
                        else:
                                continue
                if len(fourVecArray) > 1:
                        print("I have 2 real taus")
                        zvec = fourVecArray[0] + fourVecArray[1]
                        hist_array[0].Fill(zvec.M())
                        for j in range(tree.nJet):
                                total_jet +=1
                                if tree.Jet_btagDeepB[j] >= 0.4184:
                                        bjets_in_event +=1
                                        total_btagged +=1
        hist_array2[0].Fill(bjets_in_event)

print("The total amount of jets is:" , total_jet, " and the total amount of Btagged Jets is:",  total_btagged)
HistNorm(hist_array[0])
HistNorm(hist_array2[0])

ROOT.gStyle.SetOptStat(0000000)
c1=ROOT.TCanvas("","",800,600)
c1.Draw()
c1.cd()
hist_array[0].Draw("hist_same")
CMSLabel(.15,.85,ROOT.kBlack,"Internal")
c1.Print("TTBAR_DiTau_Mass.png")

c1.cd()


ROOT.gStyle.SetOptStat(0000000)
c1=ROOT.TCanvas("","",800,600)
c1.Draw()
c1.cd()
hist_array2[0].Draw("hist_same")
CMSLabel(.65,.85,ROOT.kBlack,"Internal")
c1.Print("TTBAR_Btagged_Mass.png")
c1.cd()
print("done")
                      
