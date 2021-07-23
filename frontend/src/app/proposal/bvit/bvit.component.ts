import { Component, OnInit } from '@angular/core';
import {bvit} from "./bvit-data";

@Component({
  selector: 'wm-bvit-tables',
  templateUrl: './bvit.component.html',
  styleUrls: ['./bvit.component.scss']
})
export class BvitComponent implements OnInit {
  bvit = bvit

  constructor() { }

  ngOnInit(): void {
  }

}
