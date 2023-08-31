import { Component, Input, OnInit } from "@angular/core";

import { PayloadConfigurationType } from "../../../types/observation";
import { Rss, RssExposureType } from "../../../types/rss";
import { secondsToHhMmSs } from "../../../util";
import { SoInstrumentConfiguration } from "../../so-page.component";

@Component({
  selector: "wm-rss-config-row",
  templateUrl: "./rss-config-row.component.html",
  styleUrls: ["./rss-config-row.component.scss"],
})
export class RssConfigRowComponent implements OnInit {
  @Input() instrumentConfig!: SoInstrumentConfiguration;
  rssConfig!: RssConfig;
  ngOnInit(): void {
    const rss = this.instrumentConfig.instrument as Rss;

    this.rssConfig = {
      instrumentName: this.instrumentConfig.instrumentName,
      configurationType: this.instrumentConfig.configurationType,
      exposureType: rss.detector.exposureType,
      exposureTime: rss.detector.exposureTime,
      binning: {
        preBinnedColumns: rss.detector.preBinnedColumns,
        preBinnedRows: rss.detector.preBinnedRows,
      },
      filter: rss.configuration.filter,
      lamp: this.instrumentConfig.lamp,
      cycles: rss.procedure.cycles,
      mask: rss.configuration.mask?.barcode,
      maskType: rss.configuration.mask?.maskType,
      grating: rss.configuration.spectroscopy?.grating,
      mode: rss.configuration.mode,
      gain: rss.detector.gain,
      iterations: this.instrumentConfig.iterations,
    };
  }

  protected readonly secondsToHhMmSs = secondsToHhMmSs;
}

interface RssConfig {
  instrumentName: string;
  mode: string | null;
  exposureTime: number;
  filter: string;
  gain: string;
  configurationType: PayloadConfigurationType;
  exposureType: RssExposureType;
  lamp: string | null;
  iterations: number;
  cycles: number;
  binning: { preBinnedColumns: number; preBinnedRows: number };
  mask: string | undefined;
  maskType: string | undefined;
  grating: string | undefined;
}
