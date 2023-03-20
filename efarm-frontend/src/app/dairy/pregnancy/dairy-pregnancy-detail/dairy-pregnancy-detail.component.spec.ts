import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyPregnancyDetailComponent } from './dairy-pregnancy-detail.component';

describe('DairyPregnancyDetailComponent', () => {
  let component: DairyPregnancyDetailComponent;
  let fixture: ComponentFixture<DairyPregnancyDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyPregnancyDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyPregnancyDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
