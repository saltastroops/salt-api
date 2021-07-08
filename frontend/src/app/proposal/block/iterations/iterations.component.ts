import {Component, Input, OnInit} from '@angular/core';
import {Block} from '../../../types';

@Component({
  selector: 'wm-iterations',
  templateUrl: './iterations.component.html',
  styleUrls: ['./iterations.component.scss']
})
export class IterationsComponent implements OnInit {
  @Input() block!: Block;

  constructor() { }

  ngOnInit(): void {
  }

}
