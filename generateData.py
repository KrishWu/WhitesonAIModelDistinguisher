#source /opt/homebrew/bin/thisroot.sh

import ROOT
import csv
import math

ROOT.gInterpreter.AddIncludePath("~/physics/delphes-master/external/")
ROOT.gSystem.Load("~/physics/delphes-master/libDelphes.so")

filesStr = ["300", "500", "700", "900", "1100"]
folderNames = ["MDM", "Anapole", "CR", "EDM"]

folderNameToNum = {
    "MDM": 0,
    "Anapole": 1,
    "CR": 1,
    "EDM": 0
}

massOfWBoson = 80
massOfTParticle = 172.76


with open("data/pt.csv", "w", newline='') as ptOutFile, open("data/pty.csv", "w", newline='') as ptyOutFile:
    ptOut = csv.writer(ptOutFile)
    ptyOut = csv.writer(ptyOutFile)

    for fileMassNum in filesStr:
        files = []

        for i in range(len(folderNames)):
            files.append(ROOT.TFile("./" + folderNames[i] + "/tag_1_delphes_events " + fileMassNum + ".root", "read"))

        for fileNum in range(len(files)):
            tree = files[fileNum].Get("Delphes")
            m1 = ROOT.TLorentzVector()
            m2 = ROOT.TLorentzVector()
            m3 = ROOT.TLorentzVector()

            for event in tree:
                numPhotons = event.GetLeaf("Photon", "Photon.PT").GetLen()
                if (numPhotons == 0):
                    continue

                numParticles = event.GetLeaf("Jet", "Jet.PT").GetLen()
                wBoson = ROOT.TLorentzVector()
                tParticle = ROOT.TLorentzVector()
                photon = ROOT.TLorentzVector()
                numBJets = 0
                numBJetsNegativeCharged = 0
                numNonBJets = 0
                firstRun = True
                
                #Check if not enough particles.
                if (numParticles < 3):
                    continue
                
                #Count how many of each type of particle B or notB.
                for i in range(numParticles):
                    if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 1):
                        numBJets += 1
                    else:
                        numNonBJets += 1
                
                #Check if there is enough of each type of particle notB.
                if (numNonBJets < 2 or numBJets < 1):
                    continue

                for i in range(numParticles - 1):
                    for j in range (numParticles - 1):
                        tempJ = j
                        if (j >= i):
                            tempJ += 1

                        #Check if either particle is a B particle and if so continue.
                        if (event.GetLeaf("Jet", "Jet.BTag").GetValue(i) == 1 or event.GetLeaf("Jet", "Jet.BTag").GetValue(tempJ) == 1):
                            continue
                        
                        #Calculate the mass of the W Boson and check if it is closer.
                        m1.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(i), event.GetLeaf("Jet", "Jet.Eta").GetValue(i), event.GetLeaf("Jet", "Jet.Phi").GetValue(i), event.GetLeaf("Jet", "Jet.Mass").GetValue(i))
                        m2.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(tempJ), event.GetLeaf("Jet", "Jet.Eta").GetValue(tempJ), event.GetLeaf("Jet", "Jet.Phi").GetValue(tempJ), event.GetLeaf("Jet", "Jet.Mass").GetValue(tempJ))
                        tempWBoson = m1+m2

                        for k in range(numParticles):
                            if (k == i or k == tempJ):
                                continue

                            #Check if either particle is not a B particle and if so continue.
                            # if (event.GetLeaf("Jet", "Jet.BTag").GetValue(k) == 0 or event.GetLeaf("Jet", "Jet.Charge").GetValue(k) > 0):
                            if (event.GetLeaf("Jet", "Jet.BTag").GetValue(k) == 0):
                                continue
                            #Calculate the mass of the T Particle and check if it is closer.
                            m3.SetPtEtaPhiM(event.GetLeaf("Jet", "Jet.PT").GetValue(k), event.GetLeaf("Jet", "Jet.Eta").GetValue(k), event.GetLeaf("Jet", "Jet.Phi").GetValue(k), event.GetLeaf("Jet", "Jet.Mass").GetValue(k))
                            tempTParticle = tempWBoson+m3
                            if (abs(tempTParticle.M() - massOfTParticle) + abs(tempWBoson.M() - massOfWBoson) < abs(tParticle.M() - massOfTParticle) + abs(wBoson.M() - massOfWBoson) or firstRun):
                                wBoson = tempWBoson
                                tParticle = tempTParticle
                                firstRun = False

                selectedPhoton = 0
                for i in range(numPhotons - 1):
                    if (event.GetLeaf("Photon", "Photon.PT").GetValue(i) > event.GetLeaf("Photon", "Photon.PT").GetValue(selectedPhoton + 1)):
                        selectedPhoton = i
                
                photon.SetPtEtaPhiM(event.GetLeaf("Photon", "Photon.PT").GetValue(selectedPhoton), event.GetLeaf("Photon", "Photon.Eta").GetValue(selectedPhoton), event.GetLeaf("Photon", "Photon.Phi").GetValue(selectedPhoton), 0)
                heavyTParticle = tParticle + photon

                # self.houtMassHeavyTParticle.Fill(heavyTParticle.M())
                # self.houtMomentumHeavyTParticle.Fill(heavyTParticle.Pt())
                ptOut.writerow([heavyTParticle.Pt()])
                ptyOut.writerow([folderNameToNum[folderNames[fileNum]]])

                twoQuarkDelta = tParticle.DeltaR(heavyTParticle)

                # self.houtTwoQuarkDelta.Fill(twoQuarkDelta)

                thisQuantity = math.pow((tParticle.P() + heavyTParticle.P()), 2)

                # self.houtThisQuantity.Fill(thisQuantity)
    # ROOT.gApplication.Run()