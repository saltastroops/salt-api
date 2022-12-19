// Taken from https://sankhadip.medium.com/how-to-sort-table-rows-according-column-in-angular-9-b04fdafb4140
import {
  Directive,
  ElementRef,
  HostBinding,
  HostListener,
  Input,
  Renderer2,
} from "@angular/core";

import { Sort } from "./sort";

export type SortDirection = "asc" | "desc";

@Directive({
  selector: "[wmSort]",
})
export class SortDirective {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  @Input() wmSort!: Array<any>;
  direction!: SortDirection;
  constructor(private renderer: Renderer2, private targetElem: ElementRef) {
    const elem = this.targetElem.nativeElement;
    elem.classList.add("pointer");
    elem.classList.add("sortable");
  }

  @HostListener("click")
  onClick(): void {
    // Create Object of Sort Class
    const sort = new Sort();
    // Get Reference Of Current Clicked Element
    const elem = this.targetElem.nativeElement;
    // Remove sort direction arrows on all the elements
    Array.from(this.renderer.parentNode(elem).children).forEach((child) => {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      child.classList.remove("active");
    });
    // Flip the sort direction (note that the data-order attributes the current sort
    // order)
    this.direction = elem.getAttribute("data-order") == "asc" ? "desc" : "asc";
    // Remove data-order attribute on all the elements
    Array.from(this.renderer.parentNode(elem).children).forEach((child) => {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      child.removeAttribute("data-order");
    });
    // Get The Property Type specially set [data-type=date] if it is date field
    const type = elem.getAttribute("data-type");
    // Get The Property Name from Element Attribute
    const property = elem.getAttribute("data-name");

    this.wmSort.sort(sort.startSort(property, this.direction, type));
    // Show sort direction arrows for current element
    elem.classList.add("active");
    elem.setAttribute("active", true);

    // Set the data order Element attribute
    elem.setAttribute("data-order", this.direction);
  }

  @HostBinding("class.asc")
  get sortAscending(): boolean {
    return this.direction === "asc";
  }

  @HostBinding("class.desc")
  get sortDescending(): boolean {
    return this.direction === "desc";
  }
}
