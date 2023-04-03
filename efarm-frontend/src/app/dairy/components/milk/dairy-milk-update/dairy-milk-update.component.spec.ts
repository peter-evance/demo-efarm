import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyMilkUpdateComponent } from './dairy-milk-update.component';

describe('DairyMilkUpdateComponent', () => {
  let component: DairyMilkUpdateComponent;
  let fixture: ComponentFixture<DairyMilkUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyMilkUpdateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyMilkUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
