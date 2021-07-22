import {Component, Input, OnInit} from '@angular/core';
import {Salticam} from "../../../types";


@Component({
  selector: 'wm-general',
  templateUrl: './general.component.html',
  styleUrls: ['./general.component.scss']
})
export class GeneralComponent implements OnInit {
  @Input() salticam!: Salticam;

  constructor() { }

  ngOnInit(): void {

  }

}
