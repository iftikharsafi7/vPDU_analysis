import ROOT
import os
import math

latex = ROOT.TLatex()

# Function to draw and save the plots
def draw_plot(hist_1, y_axis_title, x_axis_title, draw_grid, write_text, folder, channel_folder):
    canv = ROOT.TCanvas(str(hist_1.GetName()))
    canv.cd()
    if (draw_grid): canv.SetGrid()
    hist_1.SetLineColor(ROOT.kBlue)
    hist_1.SetLineWidth(2)
    hist_1.SetFillColor(ROOT.kGray)
    hist_1.GetYaxis().SetTitle(str(y_axis_title))
    hist_1.GetXaxis().SetTitle(str(x_axis_title))
    hist_1.SetStats(0)
    hist_1.Draw()
    # if (write_text):
    #     latex.SetNDC()
    #     latex.SetTextSize(0.05)
    #     latex.DrawText(0.6, 0.85, text)
    # Save the plot in the specified folder and channel subfolder
    canv.SaveAs(f"draw_plots_mid/{folder}/{channel_folder}/{str(hist_1.GetName())}.png")
    canv.Close()


for file_number in [501,502]:

    # Open ROOT file and get the TTree
    #in_file = ROOT.TFile.Open(f"reconstructed_root_files_with_config0/run{file_number}.root", "READ")#reconstructed_root_files_with_config0
    in_file = ROOT.TFile.Open(f"../reconstructed_root_files_rms_3/run{file_number}.root", "READ")#reconstructed_root_files_with_config0

    dstree = in_file.dstree
    number_of_channels = 8
    # Create a folder for each run
    folder_name = f"{file_number}"
    # os.system(f"mkdir -p draw_plots_mid/{folder_name}")
    # Create histograms for each channel
    hist_pk_k = ROOT.TH1F('hist_pk_k', 'Integral of the peak', 1000, 0, 0.002)
    hist_pk_p = ROOT.TH1F('hist_pk_p', 'Height of the peak', 1000, 0, 3000)
    hist_pk_p2 = ROOT.TH2F('hist_pk_p2', 'Height of the peak',200,0,40000, 1000, 250, 500)
    hist_pk_t = ROOT.TH1F('hist_pk_t', 'Time of the peak', 200, 0, 4000)
    hist_ch_bl = ROOT.TH1F('hist_ch_bl', 'Baseline of the channel', 200, 1000, 3000)
    hist_ch_rms = ROOT.TH1F('hist_ch_rms', 'RMS of the channel', 200, 0, 200)
    hist_ch_roi = ROOT.TH1F('hist_ch_roi', 'Region of interest integral', 200, -0.01, 0.01)
    hist_npeaks = ROOT.TH1F('hist_npeaks', '# of identified peaks', 101, -1, 100)

    for ch in range(0, number_of_channels):
        # Create a subfolder for each channel
        # if ch == 7 and not dstree.GetEntries(f"ch_id=={ch}"):
        #     continue
        channel_folder = f"ch_{ch}"
        os.system(f"mkdir -p draw_plots_mid/{folder_name}/{channel_folder}")

        # GET HISTOGRAMS FROM THE TREE
        dstree.Project("hist_pk_k", "pk_k", f"pk_ch=={ch}")
        dstree.Project("hist_pk_p", "pk_p", f"pk_ch=={ch}")
        dstree.Project("hist_pk_p2", "pk_p:evt_num", f"pk_ch=={ch}")
        dstree.Project("hist_pk_t", "pk_t", f"pk_ch=={ch}")
        dstree.Project("hist_ch_bl", "ch_bl", f"ch_id=={ch}")
        dstree.Project("hist_ch_rms", "ch_rms", f"ch_id=={ch}")
        dstree.Project("hist_ch_roi", "ch_roi", f"ch_id=={ch}")
        dstree.Project("hist_npeaks", "npeaks", f"ch_id=={ch}")
       

        # Draw and save the plots in the specific folder and channel subfolder
        draw_plot(hist_pk_k, "Peaks", "Integral", False, True, folder_name, channel_folder)
        draw_plot(hist_pk_p, "Peaks", "Amplitude", False, True, folder_name, channel_folder)
        draw_plot(hist_pk_p2, "Amplitude", "peaks", False, True, folder_name, channel_folder)
        draw_plot(hist_pk_t, "Peaks", "Time [samples]", False, True, folder_name, channel_folder)
        draw_plot(hist_ch_bl, "Events", "Baseline", False, True, folder_name, channel_folder)
        draw_plot(hist_ch_rms, "Events", "RMS", False, True, folder_name, channel_folder)
        draw_plot(hist_ch_roi, "Events", "ROI integral", False, True, folder_name, channel_folder)
        draw_plot(hist_npeaks, "Events", "Identified peaks", False, True, folder_name, channel_folder)

# Close the ROOT file
in_file.Close()
