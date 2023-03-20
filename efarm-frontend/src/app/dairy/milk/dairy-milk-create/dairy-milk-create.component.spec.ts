import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyMilkCreateComponent } from './dairy-milk-create.component';

describe('DairyMilkCreateComponent', () => {
  let component: DairyMilkCreateComponent;
  let fixture: ComponentFixture<DairyMilkCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyMilkCreateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyMilkCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
