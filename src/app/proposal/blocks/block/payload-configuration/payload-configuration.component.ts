import { Component, Input, OnChanges } from "@angular/core";

import {
  PayloadConfiguration,
  TelescopeConfiguration,
} from "../../../../types/observation";

@Component({
  selector: "wm-payload",
  templateUrl: "./payload-configuration.component.html",
  styleUrls: ["./payload-configuration.component.scss"],
})
export class PayloadConfigurationComponent implements OnChanges {
  @Input() telescopeConfiguration!: TelescopeConfiguration;
  @Input() payloadConfigurationIndex!: number;

  payloadConfiguration!: PayloadConfiguration;
  instrument!: string;
  headerLine: string | null = null;
  ditherPatternDescription!: string;

  ngOnChanges(): void {
    this.payloadConfiguration =
      this.telescopeConfiguration.payloadConfigurations[
        this.payloadConfigurationIndex
      ];

    const instruments = this.payloadConfiguration.instruments;
    if (instruments.salticam) {
      this.instrument = "Salticam";
    } else if (instruments.rss) {
      this.instrument = "RSS";
    } else if (instruments.hrs) {
      this.instrument = "HRS";
    } else if (instruments.bvit) {
      this.instrument = "BVIT";
    } else if (instruments.nir) {
      this.instrument = "NIR";
    }

    this.headerLine = this.instrument.toLowerCase() + "-";
    if (
      this.payloadConfiguration.payloadConfigurationType ===
      "Instrument Acquisition"
    ) {
      this.headerLine += "acquisition";
    } else if (this.payloadConfiguration.payloadConfigurationType) {
      this.headerLine +=
        this.payloadConfiguration.payloadConfigurationType.toLowerCase();
    } else {
      this.headerLine += "unknown";
    }
    this.headerLine += "-config-color";

    const dp = this.telescopeConfiguration.ditherPattern;
    this.ditherPatternDescription = dp
      ? `${dp.horizontalTiles} h.t. x ${
          dp.verticalTiles
        } v.t., ${dp.offsetSize.toFixed(1)} arcsec, ${dp.steps} dithers`
      : "";
  }

  headerLineBackgroundColor(): void {
    switch (this.payloadConfiguration.payloadConfigurationType) {
      case "Science":
        this.headerLine = "rss-config-color";
        break;
      case "Calibration":
        this.headerLine = "rss--config-color";
        break;
      case "Acquisition":
        this.headerLine = "rss-header-config-color";
        break;
    }
  }
}
