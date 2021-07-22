import { Component, OnInit, Input } from '@angular/core';
import {salticam} from "./salticam-data";

@Component({
  selector: 'wm-salticam',
  templateUrl: './salticam.component.html',
  styleUrls: ['./salticam.component.scss']
})
export class SalticamComponent implements OnInit {
  salticam = salticam;

  constructor() { }

  ngOnInit(): void {
  }

}

