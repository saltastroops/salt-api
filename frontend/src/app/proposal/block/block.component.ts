import {Component, Input, OnInit} from '@angular/core';
import {Block} from '../../types';

@Component({
  selector: 'wm-block',
  templateUrl: './block.component.html',
  styleUrls: ['./block.component.scss']
})
export class BlockComponent implements OnInit {
  @Input() block!: Block;
  constructor() { }

  ngOnInit(): void {
  }

}
