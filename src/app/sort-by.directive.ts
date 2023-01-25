import {
  Directive,
  ElementRef,
  HostListener,
  Input,
  OnInit,
} from "@angular/core";

/**
 * A directive for making a table column sortable.
 *
 * This directive should be added to a table header (th) element, and it has to be used
 * together with the wmSort directive. See the documentation of that directive for more
 * details.
 *
 * The directive adds "pointer" and "sortable" to the class attribute of the host
 * element. It also adds data-sort-key and data-sort-direction attributes. These should
 * be considered internal and should not be modified.
 */
@Directive({
  selector: "[wmSortBy]",
})
export class SortByDirective implements OnInit {
  @Input() wmSortBy!: string;

  constructor(private targetElem: ElementRef) {}

  ngOnInit(): void {
    const elem = this.targetElem.nativeElement;
    elem.classList.add("pointer");
    elem.classList.add("sortable");
    elem.setAttribute("data-sort-key", this.wmSortBy);
    elem.setAttribute("data-sort-direction", "desc");
  }

  @HostListener("click", ["$event"])
  onClick(event: Event): void {
    if (event.target === null) return;
    event.target.dispatchEvent(
      new CustomEvent("sortByColumn", { bubbles: true, detail: this.wmSortBy }),
    );
  }
}
