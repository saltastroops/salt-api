import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-polarimetric-imaging-table',
  templateUrl: './polarimetric-imaging-table.component.html',
  styleUrls: ['./polarimetric-imaging-table.component.scss']
})
export class PolarimetricImagingTableComponent implements OnInit {
  @Input() polorimetryImaging: PolarimetricImaging = {
    filter: 'pi0000',
    beamSplitterOrientation: 'Normal'
  };
  constructor() { }

  ngOnInit(): void {
  }

}

// TODO this should go to the RSS Types
interface PolarimetricImaging {
  filter: string;  // TODO this should be an enum
  beamSplitterOrientation: string;  // TODO this should be an enum
}
