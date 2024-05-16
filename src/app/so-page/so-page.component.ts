import { Component, OnInit } from "@angular/core";

import { of } from "rxjs";
import { catchError, switchMap, tap } from "rxjs/operators";

import { ProposalService } from "../service/proposal.service";
import { SoService } from "../service/so.service";
import { Block } from "../types/block";
import { Lamp } from "../types/common";
import { Hrs } from "../types/hrs";
import { Nir } from "../types/nir";
import { PayloadConfigurationType } from "../types/observation";
import { Proposal } from "../types/proposal";
import { Rss } from "../types/rss";
import { Salticam } from "../types/salticam";
import { Acquisition } from "../types/so";
import { AutoUnsubscribe, GENERIC_ERROR_MESSAGE } from "../utils";

@Component({
  selector: "wm-so-page",
  templateUrl: "./so-page.component.html",
  styleUrls: ["./so-page.component.scss"],
})
@AutoUnsubscribe()
export class SoPageComponent implements OnInit {
  block: Block | undefined;
  proposal: Proposal | undefined;
  error: string | undefined = "This is fake error";
  acquisition!: Acquisition;
  telescopeConfigurations!: SoInstrumentConfiguration[];
  positionAngle: number | null = null;
  loading = false;
  automaticallyUpdate = false;
  loadBlock = "currentBlock";
  initialLoad = false;
  constructor(
    private soService: SoService,
    private proposalService: ProposalService,
  ) {}

  ngOnInit(): void {
    this.initialLoad = true;
    this.loading = true;
    this.fetchBlock();
    setInterval(() => {
      if (this.automaticallyUpdate) {
        this.fetchBlock();
      }
    }, 60000);
  }

  fetchBlock(): void {
    this.telescopeConfigurations = [];
    this.error = undefined;
    const loadedBlock$ =
      this.loadBlock === "currentBlock"
        ? this.soService.getCurrentBlock()
        : this.soService.getNextScheduledBlock();
    loadedBlock$
      .pipe(
        tap((block) => {
          if (block) {
            this.createConfiguration(block);
          } else {
            this.block = undefined;
          }
          this.loading = false;
        }),
        switchMap(() => {
          if (this.block) {
            return this.proposalService.getProposal(this.block.proposalCode);
          }

          return of(undefined);
        }),
        catchError((err) => {
          this.loading = false;
          if (err.status === 404) {
            if (this.loadBlock === "currentBlock") {
              this.error =
                "There is no block that is being observed currently.";
            } else {
              this.error =
                "There is no block that is scheduled for the next observation.";
            }
          } else {
            this.error = GENERIC_ERROR_MESSAGE;
          }

          return of(undefined);
        }),
      )
      .subscribe((proposal) => {
        this.proposal = proposal;
      });
  }

  updatePage(): void {
    this.initialLoad = false;
    this.loading = true;
    this.fetchBlock();
  }
  updateAutomatically(checked: boolean): void {
    this.automaticallyUpdate = checked;
  }

  displayedBlockChange(loadBlockValue: string): void {
    this.loadBlock = loadBlockValue;
    this.updatePage();
  }

  createConfiguration(block: Block): void {
    const acquisition: any = {};
    acquisition["maximumSeeing"] = block.observingConditions.maximumSeeing;
    block.observations.forEach((o) => {
      acquisition["targetName"] = o.target.name;
      acquisition["finderCharts"] = o.finderCharts;
      o.telescopeConfigurations.forEach((tc) => {
        acquisition["guideStar"] = tc.guideStar;
        this.positionAngle = tc.positionAngle;
        tc.payloadConfigurations.forEach((pc, payloadConfigIndex) => {
          const telescopeConfig = {
            configurationType: pc.payloadConfigurationType,
            iterations: tc.iterations,
            lamp: pc.lamp,
            calibrationFilter: pc.calibrationFilter
          };

          if (pc.instruments.salticam) {
            pc.instruments.salticam.forEach((scam) => {
              this.telescopeConfigurations.push({
                ...telescopeConfig,
                instrumentName: "Salticam",
                instrument: scam,
                payloadConfigIndex,
              });
            });
          }
          if (pc.instruments.rss) {
            pc.instruments.rss.forEach((rss) => {
              this.telescopeConfigurations.push({
                ...telescopeConfig,
                instrumentName: "RSS",
                instrument: rss,
                payloadConfigIndex,
              });
            });
          }
          if (pc.instruments.hrs) {
            pc.instruments.hrs.forEach((hrs) => {
              this.telescopeConfigurations.push({
                ...telescopeConfig,
                instrumentName: "HRS",
                instrument: hrs,
                payloadConfigIndex,
              });
            });
          }
          if (pc.instruments.nir) {
            pc.instruments.nir.forEach((nir: Nir) => {
              this.telescopeConfigurations.push({
                ...telescopeConfig,
                instrumentName: "NIR",
                instrument: nir,
                payloadConfigIndex,
              });
            });
          }
        });
      });
    });
    this.block = block;
    this.acquisition = acquisition;
  }
}

export interface SoInstrumentConfiguration {
  instrumentName: string;
  configurationType: PayloadConfigurationType;
  lamp: Lamp | null;
  calibrationFilter: string | null;
  iterations: number;
  instrument: Hrs | Nir | Rss | Salticam;
  payloadConfigIndex: number;
}
