import {
  Directive,
  ElementRef,
  HostListener,
  Input,
  Renderer2,
} from "@angular/core";

export type SortDirection = "asc" | "desc";

/**
 * A directive for sorting table content.
 *
 * The directive should be added to a table element, and its value must be a function
 * that accepts a string and a boolean as its only arguments. This function is supposed
 * to be a sort function. Its first argument is supposed to be a sort key, and its
 * second arguments indicates the sort direction. For example, if a component has a
 * member function
 *
 * f = (key: string, direction: SortDirection) => {
 *   // do some sorting
 * }
 *
 * then you would use the directive as follows:
 *
 * <table [wmSort]="f">...</table>
 *
 * Note that f is defined via f = (...) => {...}; if it was defined via f(...) {...} the
 * scope of this would be the directive rather than the component.
 *
 * The wmSort directive must be used together with wmSortBy directives on table headers.
 * The wmSortBy directive makes the table column sortable. It is used with a string
 * value, and the sort function of the wmSort directive is called with this value when
 * the table header is clicked. For example, consider the following table:
 *
 * <table [wmSort]="f">
 *   <tr>
 *     <th wmSortBy="name">Name</th>
 *     <th wmSortBy="priority">Priority</th>
 *   </tr>
 *  <tr>
 *     <td>Block 1</td>
 *     <td>2</td>
 *   </tr>
 *   <tr>
 *     <td>Block 2</td>
 *     <td>1</td>
 *   </tr>
 * </table>
 *
 * Then if the Name column header is clicked, f will be called as f("Name", "asc"), and
 * when the header is clicked again, f will be called as f("Name", "desc").
 *
 * If the table is sorted by a column, "active" and "asc" (for ascending sort direction)
 * or "active" and "desc" (for descending sort direction) are added to the class
 * attribute of the element with the respective wmSortBy directive value.
 */
@Directive({
  selector: "[wmSort]",
})
export class SortDirective {
  @Input() wmSort!: (key: string, sortOrder: SortDirection) => void;

  direction: SortDirection = "desc";

  constructor(private renderer: Renderer2, private targetElem: ElementRef) {}

  @HostListener("sortByColumn", ["$event"])
  onSortByColumn(event: CustomEvent): void {
    // Get the selected header...
    const sortKey = event.detail;
    const elem = this.targetElem.nativeElement;
    const selectedSortableHeader = elem.querySelector(
      `[data-sort-key=${sortKey}]`,
    );

    // ... and its current sort direction
    const currentSortDirection = selectedSortableHeader.getAttribute(
      "data-sort-direction",
    );

    // Flip the sort direction
    this.direction = currentSortDirection == "asc" ? "desc" : "asc";

    // Perform the sorting
    this.wmSort(event.detail, this.direction);

    // Reset all the sortable column headers
    const sortableHeaders = elem.querySelectorAll("[data-sort-key]");
    sortableHeaders.forEach((e: Element) => {
      e.setAttribute("data-sort-direction", "desc");
      e.classList.remove("active", "asc", "desc");
    });

    // Update the selected header
    selectedSortableHeader.setAttribute("data-sort-direction", this.direction);
    selectedSortableHeader.classList.add("active");
    selectedSortableHeader.classList.add(this.direction);
  }
}
