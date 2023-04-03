import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyPregnancyUpdateComponent } from './dairy-pregnancy-update.component';

describe('DairyPregnancyUpdateComponent', () => {
  let component: DairyPregnancyUpdateComponent;
  let fixture: ComponentFixture<DairyPregnancyUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyPregnancyUpdateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyPregnancyUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
