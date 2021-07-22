import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-fabry-perot-table',
  templateUrl: './fabry-perot-table.component.html',
  styleUrls: ['./fabry-perot-table.component.scss']
})
export class FabryPerotTableComponent implements OnInit {
  @Input() fabryPerot: FabryPerot = {
    filter: 'pi0000',
    mode: 'Low resolution'
  };
  constructor() { }

  ngOnInit(): void {
  }

}

interface FabryPerot {
  filter: string;
  mode: string;  // TODO this should be an enum
}
