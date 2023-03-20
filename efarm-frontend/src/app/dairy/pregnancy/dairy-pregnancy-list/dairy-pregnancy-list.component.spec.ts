import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyPregnancyListComponent } from './dairy-pregnancy-list.component';

describe('DairyPregnancyListComponent', () => {
  let component: DairyPregnancyListComponent;
  let fixture: ComponentFixture<DairyPregnancyListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyPregnancyListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyPregnancyListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
