import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyLactationListComponent } from './dairy-lactation-list.component';

describe('DairyLactationListComponent', () => {
  let component: DairyLactationListComponent;
  let fixture: ComponentFixture<DairyLactationListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyLactationListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyLactationListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
