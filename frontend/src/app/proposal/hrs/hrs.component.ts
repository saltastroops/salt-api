import {Component, OnInit} from '@angular/core';
import {hrs} from "./hrs-data";


@Component({
  selector: 'wm-hrs',
  templateUrl: './hrs.component.html',
  styleUrls: ['./hrs.component.scss']
})
export class HrsComponent implements OnInit {
  hrs = hrs;

  constructor() { }

  ngOnInit(): void {
  }

}
